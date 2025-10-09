from django import forms
from .models import CasoDeUso

class CasoDeUsoForm(forms.ModelForm):
    class Meta:
        model = CasoDeUso
        fields = ['nombre', 'descripcion', 'proyecto']
