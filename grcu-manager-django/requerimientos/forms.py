from django import forms
from django.core.exceptions import ValidationError
from datetime import date
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
    FUENTE_CHOICES = [
        ('', '-- Seleccionar fuente --'),
        ('ENTREVISTA_STAKEHOLDER', 'Entrevista con stakeholder/Cliente'),
        ('DOCUMENTO_REQUERIMIENTOS', 'Documento de requerimientos'),
        ('OBSERVACION_USUARIO', 'Observación de usuario'),
        ('ENCUESTA_CUESTIONARIO', 'Encuesta / Cuestionario'),
        ('ANALISIS_SISTEMA', 'Análisis de sistema existente'),
        ('SOLICITUD_CLIENTE', 'Solicitud del cliente'),
        ('OTRO', 'Otro (especificar)'),
    ]
    
    fuente = forms.ChoiceField(
        choices=FUENTE_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'id_fuente_select'
        }),
        label='Fuente',
        help_text='Origen del requerimiento'
    )
    
    fuente_otro = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Especifique la fuente',
            'id': 'id_fuente_otro'
        }),
        label='Especificar fuente'
    )
    
    CATEGORIA_CHOICES = [
        ('', '-- Seleccionar categoría --'),
        ('SEGURIDAD', 'Seguridad'),
        ('RENDIMIENTO', 'Rendimiento'),
        ('USABILIDAD', 'Usabilidad'),
        ('MANTENIBILIDAD', 'Mantenibilidad'),
        ('COMPATIBILIDAD', 'Compatibilidad'),
        ('DISPONIBILIDAD', 'Disponibilidad'),
        ('ESCALABILIDAD', 'Escalabilidad'),
        ('CONFIABILIDAD', 'Confiabilidad'),
        ('OTRO', 'Otro (especificar)'),
    ]
    
    categoria = forms.ChoiceField(
        choices=CATEGORIA_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'id_categoria_select'
        }),
        label='Categoría'
    )
    
    categoria_otro = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Especifique la categoría',
            'id': 'id_categoria_otro'
        }),
        label='Especificar categoría'
    )
    
    fecha_compromiso = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'min': date.today().isoformat()  # No permite fechas pasadas
        }),
        label='Fecha de Compromiso',
        help_text='Fecha estimada de entrega (no puede ser en el pasado)'
    )
    
    def clean_fecha_compromiso(self):
        """Validar que la fecha de compromiso no sea en el pasado"""
        fecha = self.cleaned_data.get('fecha_compromiso')
        if fecha and fecha < date.today():
            raise ValidationError('La fecha de compromiso no puede ser anterior a hoy.')
        return fecha
    
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
