from django import forms
from proyectos.models import Proyecto
from grupos.models import Grupo
from accounts.models import Usuario

class ProyectoCrearForm(forms.ModelForm):
    grupo = forms.ModelChoiceField(
        queryset=Grupo.objects.filter(activo=True),
        empty_label="Sin grupo asignado (opcional)",
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_grupo'}),
        required=False
    )

    lider = forms.ChoiceField(
        choices=[],
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_lider'}),
        required=False  # Hacer opcional cuando no hay grupo
    )

    clientes = forms.MultipleChoiceField(
        choices=[],
        widget=forms.SelectMultiple(attrs={'class': 'form-control', 'id': 'id_clientes', 'size': '5'}),
        required=False,
        label='Clientes/Stakeholders',
        help_text='Selecciona uno o más clientes para este proyecto (mantén Ctrl/Cmd para seleccionar múltiples)'
    )

    visitantes = forms.MultipleChoiceField(
        choices=[],
        widget=forms.SelectMultiple(attrs={'class': 'form-control', 'id': 'id_visitantes', 'size': '5'}),
        required=False,
        label='Visitantes',
        help_text='Selecciona uno o más visitantes para este proyecto (acceso de solo lectura)'
    )

    class Meta:
        model = Proyecto
        fields = ['nombre', 'descripcion', 'logo', 'grupo', 'clientes', 'visitantes']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'logo': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Inicializar choices vacíos para lider, clientes y visitantes
        self.fields['lider'].choices = []
        self.fields['clientes'].choices = []
        self.fields['visitantes'].choices = []

        # Cargar clientes disponibles (usuarios con rol Stakeholder)
        stakeholders = Usuario.objects.filter(roles__nombre='Stakeholder').distinct().order_by('nombre')
        self.fields['clientes'].choices = [
            (usuario.pk, f"{usuario.nombre} ({usuario.email})")
            for usuario in stakeholders
        ]

        # Cargar visitantes disponibles (usuarios con rol Visitante)
        visitantes = Usuario.objects.filter(roles__nombre='Visitante').distinct().order_by('nombre')
        self.fields['visitantes'].choices = [
            (usuario.pk, f"{usuario.nombre} ({usuario.email})")
            for usuario in visitantes
        ]

        # Si hay un grupo seleccionado, cargar sus integrantes
        if 'grupo' in self.data and self.data['grupo']:
            try:
                grupo_id = int(self.data['grupo'])
                grupo = Grupo.objects.get(id=grupo_id, activo=True)
                integrantes = grupo.integrantes.all().order_by('nombre')
                self.fields['lider'].choices = [
                    (usuario.id, f"{usuario.nombre} ({usuario.email})")
                    for usuario in integrantes
                ]
                self.fields['lider'].required = True  # Requerir lider cuando hay grupo
            except (ValueError, Grupo.DoesNotExist):
                pass
        elif self.instance and self.instance.pk and self.instance.grupo:
            # Para edición, cargar integrantes del grupo actual
            integrantes = self.instance.grupo.integrantes.all().order_by('nombre')
            self.fields['lider'].choices = [
                (usuario.id, f"{usuario.nombre} ({usuario.email})")
                for usuario in integrantes
            ]
            # Seleccionar el lider actual
            if self.instance.lider:
                self.initial['lider'] = self.instance.lider.id
            self.fields['lider'].required = True  # Requerir lider cuando hay grupo
        else:
            # No hay grupo seleccionado
            self.fields['lider'].required = False  # No requerir lider cuando no hay grupo
        
        # Si estamos editando, preseleccionar los clientes y visitantes actuales
        if self.instance and self.instance.pk:
            self.initial['clientes'] = list(self.instance.clientes.values_list('id', flat=True))
            self.initial['visitantes'] = list(self.instance.visitantes.values_list('id', flat=True))

    def clean(self):
        cleaned_data = super().clean()
        grupo = cleaned_data.get('grupo')
        lider = cleaned_data.get('lider')
        clientes_ids = cleaned_data.get('clientes')

        # Si hay grupo seleccionado, debe haber lider
        if grupo and not lider:
            self.add_error('lider', "Por favor, selecciona un líder del grupo. El campo de líder se llena automáticamente cuando seleccionas un grupo.")
            raise forms.ValidationError("Debe seleccionar un líder cuando hay un grupo asignado.")

        # Si hay lider seleccionado, debe haber grupo
        if lider and not grupo:
            self.add_error('grupo', "No puedes seleccionar un líder sin asignar primero un grupo.")
            raise forms.ValidationError("No puede seleccionar un líder sin asignar un grupo.")

        # Validar que los clientes NO pertenezcan al grupo de desarrollo
        if grupo and clientes_ids:
            # Convertir IDs de clientes (strings) a objetos Usuario
            clientes_ids_int = [int(id) for id in clientes_ids]
            clientes_objs = Usuario.objects.filter(id__in=clientes_ids_int)
            
            integrantes_grupo = set(grupo.integrantes.all())
            clientes_set = set(clientes_objs)
            clientes_en_grupo = integrantes_grupo.intersection(clientes_set)
            
            if clientes_en_grupo:
                nombres = ', '.join([u.nombre for u in clientes_en_grupo])
                raise forms.ValidationError(
                    f"Los siguientes clientes no pueden ser asignados porque pertenecen al grupo de desarrollo: {nombres}"
                )

        return cleaned_data