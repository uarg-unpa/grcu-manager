from django import forms
from .models import CasoDeUso, DetalleCasoDeUsoTradicional, DetalleCasoDeUsoAgil

class CasoDeUsoForm(forms.ModelForm):
    class Meta:
        model = CasoDeUso
        fields = ['nombre', 'descripcion', 'proyecto']

# ============================================================================
# FORMULARIOS ESPECÍFICOS POR METODOLOGÍA
# ============================================================================

class CasoDeUsoTradicionalForm(forms.Form):
    """
    Formulario para crear casos de uso con metodología TRADICIONAL.
    Incluye campos comunes + campos específicos del detalle tradicional.
    """
    # Campos comunes del Caso de Uso
    nombre = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: Registrar nuevo usuario'
        }),
        label='Nombre del Caso de Uso'
    )
    
    descripcion = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Descripción general del caso de uso...'
        }),
        label='Descripción'
    )
    
    # Campos específicos del DetalleCasoDeUsoTradicional
    actor_principal = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: Usuario registrado, Administrador'
        }),
        label='Actor Principal',
        help_text='Quién interactúa con este caso de uso'
    )
    
    precondiciones = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Condiciones que deben cumplirse antes de ejecutar el caso de uso...'
        }),
        label='Precondiciones'
    )
    
    flujo_principal = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5,
            'placeholder': '1. El usuario accede a...\n2. El sistema muestra...\n3. El usuario selecciona...'
        }),
        label='Flujo Principal',
        help_text='Secuencia normal de pasos'
    )
    
    flujo_alternativo = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Flujos alternativos o excepcionales...'
        }),
        label='Flujo Alternativo'
    )
    
    postcondiciones = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Estado del sistema después de ejecutar el caso de uso...'
        }),
        label='Postcondiciones'
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
            'placeholder': 'https://ejemplo.com/diagrama'
        }),
        label='Enlace a Recurso Externo',
        help_text='URL completa del recurso externo'
    )


class CasoDeUsoAgilForm(forms.Form):
    """
    Formulario para crear casos de uso con metodología ÁGIL.
    Incluye campos comunes + campos específicos del detalle ágil.
    """
    # Campos comunes del Caso de Uso
    nombre = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: Autenticación con OAuth'
        }),
        label='Nombre del Caso de Uso'
    )
    
    descripcion = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Descripción breve del caso de uso...'
        }),
        label='Descripción'
    )
    
    # Campos específicos del DetalleCasoDeUsoAgil
    historia_usuario = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Como [usuario]\nQuiero [funcionalidad]\nPara [beneficio]'
        }),
        label='Historia de Usuario',
        help_text='Formato: Como... Quiero... Para...'
    )
    
    criterio_aceptacion = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': '- Dado que...\n- Cuando...\n- Entonces...'
        }),
        label='Criterios de Aceptación'
    )
    
    responsable = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nombre del responsable'
        }),
        label='Responsable'
    )
    
    ESTADO_SCRUM_CHOICES = [
        ('', '-- Seleccionar estado --'),
        ('BACKLOG', 'Product Backlog'),
        ('TODO', 'To Do'),
        ('IN_PROGRESS', 'In Progress'),
        ('IN_REVIEW', 'In Review'),
        ('DONE', 'Done')
    ]
    
    estado_scrum = forms.ChoiceField(
        choices=ESTADO_SCRUM_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Estado Scrum',
        initial='BACKLOG'
    )
    
    observaciones = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Notas adicionales...'
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
            'placeholder': 'https://ejemplo.com/diagrama'
        }),
        label='Enlace a Recurso Externo',
        help_text='URL completa del recurso externo'
    )

