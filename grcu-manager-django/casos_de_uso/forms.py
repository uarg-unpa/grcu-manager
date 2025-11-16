from django import forms
from .models import CasoDeUso, DetalleCasoDeUsoTradicional, DetalleCasoDeUsoAgil

class CasoDeUsoForm(forms.ModelForm):
    class Meta:
        model = CasoDeUso
        fields = ['nombre', 'descripcion', 'proyecto']

# ============================================================================
# FORMULARIOS ESPECÍFICOS POR METODOLOGÍA
# ============================================================================


# Formulario unificado para casos de uso
class CasoDeUsoUnificadoForm(forms.Form):
    identificador = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'readonly': 'readonly',
            'placeholder': 'CU-XXX'
        }),
        label='Identificador',
        help_text='Se genera automáticamente'
    )
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
