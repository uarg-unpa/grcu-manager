from django import forms
from proyectos.models import Proyecto
from grupos.models import Grupo

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

    class Meta:
        model = Proyecto
        fields = ['nombre', 'descripcion', 'metodologia', 'logo', 'grupo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'metodologia': forms.Select(attrs={'class': 'form-control'}),
            'logo': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Inicializar choices vacíos para lider
        self.fields['lider'].choices = []

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

    def clean(self):
        cleaned_data = super().clean()
        grupo = cleaned_data.get('grupo')
        lider = cleaned_data.get('lider')

        # Si hay grupo seleccionado, debe haber lider
        if grupo and not lider:
            raise forms.ValidationError("Debe seleccionar un líder cuando hay un grupo asignado.")

        # Si hay lider seleccionado, debe haber grupo
        if lider and not grupo:
            raise forms.ValidationError("No puede seleccionar un líder sin asignar un grupo.")

        return cleaned_data