from django import forms
from .models import Requerimiento, DetalleRequerimientoTradicional, DetalleRequerimientoAgil

class RequerimientoForm(forms.ModelForm):
    class Meta:
        model = Requerimiento
        fields = ['nombre', 'descripcion', 'tipo', 'estado', 'proyecto']


# ============================================================================
# FORMULARIOS ESPECÍFICOS POR METODOLOGÍA
# ============================================================================

class RequerimientoTradicionalForm(forms.Form):
    """
    Formulario para crear requerimientos con metodología TRADICIONAL.
    Incluye campos comunes + campos específicos del detalle tradicional.
    """
    # Campos comunes del Requerimiento
    nombre = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: Sistema de autenticación de usuarios'
        }),
        label='Nombre del Requerimiento'
    )
    
    descripcion = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Descripción detallada del requerimiento...'
        }),
        label='Descripción'
    )
    
    tipo = forms.ChoiceField(
        choices=Requerimiento.TIPO_CHOICES,
        required=True,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        label='Tipo de Requerimiento',
        initial='FUNCIONAL'
    )
    
    # Campos específicos del DetalleRequerimientoTradicional
    PRIORIDAD_MOSCOW = [
        ('', '-- Seleccionar prioridad --'),
        ('MUST', 'Must have (Debe tener)'),
        ('SHOULD', 'Should have (Debería tener)'),
        ('COULD', 'Could have (Podría tener)'),
        ('WONT', "Won't have (No tendrá por ahora)")
    ]
    
    prioridad = forms.ChoiceField(
        choices=PRIORIDAD_MOSCOW,
        required=False,  # La prioridad se asigna en la fase de priorización
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Prioridad (MoSCoW)',
        help_text='La prioridad se asigna después de la validación del requerimiento'
    )
    
    fuente = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: Entrevista con stakeholder, Documento de requisitos'
        }),
        label='Fuente',
        help_text='Origen del requerimiento'
    )
    
    categoria = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: Seguridad, Rendimiento, Usabilidad'
        }),
        label='Categoría'
    )
    
    fecha_compromiso = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }),
        label='Fecha de Compromiso',
        help_text='Fecha estimada de entrega'
    )
    
    ESTADO_VALIDACION_CHOICES = [
        ('', '-- Seleccionar estado --'),
        ('PENDIENTE', 'Pendiente de validación'),
        ('EN_REVISION', 'En revisión'),
        ('APROBADO', 'Aprobado'),
        ('RECHAZADO', 'Rechazado'),
        ('REQUIERE_CAMBIOS', 'Requiere cambios')
    ]
    
    estado_validacion = forms.ChoiceField(
        choices=ESTADO_VALIDACION_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Estado de Validación'
    )
    
    observaciones = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Observaciones adicionales...'
        }),
        label='Observaciones'
    )
    
    # Campos para adjuntos y recursos externos
    imagen = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': 'image/png,image/jpeg,image/jpg'
        }),
        label='Imagen Adjunta',
        help_text='Formatos permitidos: PNG, JPG, JPEG (máx. 5MB)'
    )
    
    link_externo = forms.URLField(
        required=False,
        widget=forms.URLInput(attrs={
            'class': 'form-control',
            'placeholder': 'https://ejemplo.com/recurso'
        }),
        label='Enlace a Recurso Externo',
        help_text='URL completa del recurso externo'
    )


class RequerimientoAgilForm(forms.Form):
    """
    Formulario para crear requerimientos con metodología ÁGIL.
    Incluye campos comunes + campos específicos del detalle ágil (User Story).
    """
    # Campos comunes del Requerimiento
    nombre = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: Login de usuarios con redes sociales'
        }),
        label='Nombre de la User Story'
    )
    
    descripcion = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Descripción breve de la funcionalidad...'
        }),
        label='Descripción'
    )
    
    tipo = forms.ChoiceField(
        choices=Requerimiento.TIPO_CHOICES,
        required=True,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        label='Tipo de Requerimiento',
        initial='FUNCIONAL'
    )
    
    # Campos específicos del DetalleRequerimientoAgil
    historia_usuario = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Como [tipo de usuario]\nQuiero [realizar alguna acción]\nPara [obtener algún beneficio]'
        }),
        label='Historia de Usuario',
        help_text='Formato: Como... Quiero... Para...'
    )
    
    criterio_aceptacion = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': '- Dado que [contexto inicial]\n- Cuando [acción que ocurre]\n- Entonces [resultado esperado]'
        }),
        label='Criterios de Aceptación',
        help_text='Define cuándo la historia está completa'
    )
    
    STORY_POINTS_CHOICES = [
        ('', '-- Sin estimar --'),
        (1, '1 punto'),
        (2, '2 puntos'),
        (3, '3 puntos'),
        (5, '5 puntos'),
        (8, '8 puntos'),
        (13, '13 puntos'),
        (21, '21 puntos')
    ]
    
    puntos_estimados = forms.TypedChoiceField(
        choices=STORY_POINTS_CHOICES,
        required=False,
        coerce=lambda x: int(x) if x else None,
        empty_value=None,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Story Points',
        help_text='Estimación de esfuerzo (Fibonacci)'
    )
    
    observaciones = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Notas adicionales sobre la historia...'
        }),
        label='Observaciones'
    )
    
    # Campos para adjuntos y recursos externos
    imagen = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': 'image/png,image/jpeg,image/jpg'
        }),
        label='Imagen Adjunta',
        help_text='Formatos permitidos: PNG, JPG, JPEG (máx. 5MB)'
    )
    
    link_externo = forms.URLField(
        required=False,
        widget=forms.URLInput(attrs={
            'class': 'form-control',
            'placeholder': 'https://ejemplo.com/recurso'
        }),
        label='Enlace a Recurso Externo',
        help_text='URL completa del recurso externo'
    )
