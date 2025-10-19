from django import forms
from .models import Grupo

class GrupoForm(forms.ModelForm):
    class Meta:
        model = Grupo
        fields = ['nombre', 'logo', 'activo']
        widgets = {
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
