from django import forms
from .models import Grupo

class GrupoForm(forms.ModelForm):
    class Meta:
        model = Grupo
        fields = ['nombre', 'logo', 'activo', 'integrantes']
        widgets = {
            'integrantes': forms.SelectMultiple(attrs={'size': 8}),
        }
