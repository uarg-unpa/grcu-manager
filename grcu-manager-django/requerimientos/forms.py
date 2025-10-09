from django import forms
from .models import Requerimiento

class RequerimientoForm(forms.ModelForm):
    class Meta:
        model = Requerimiento
        fields = ['nombre', 'descripcion', 'tipo', 'estado', 'proyecto']
