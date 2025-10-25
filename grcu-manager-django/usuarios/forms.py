from django import forms
from accounts.models import Usuario  # Usuario está en accounts, no en usuarios
from roles.models import Rol
from django.core.exceptions import ValidationError

class UsuarioCrearForm(forms.ModelForm):
    roles = forms.ModelMultipleChoiceField(
        queryset=Rol.objects.filter(nombre__in=["Admin", "Desarrollador"]),  # Roles Admin y Desarrollador disponibles
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    password = forms.CharField(widget=forms.HiddenInput(), required=False)  # opcional

    class Meta:
        model = Usuario
        fields = ["email", "roles", "is_active"]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not email:
            raise ValidationError("El email es obligatorio.")
        if not email.lower().endswith("@gmail.com"):
            raise ValidationError("Solo se permiten correos de Gmail.")
        return email


class UsuarioEditarForm(forms.ModelForm):
    roles = forms.ModelMultipleChoiceField(
        queryset=Rol.objects.filter(nombre__in=["Admin", "Desarrollador"]),  # Roles Admin y Desarrollador disponibles
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Usuario
        fields = ["email", "roles", "is_active"]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not email:
            raise ValidationError("El email es obligatorio.")
        if not email.lower().endswith("@gmail.com"):
            raise ValidationError("Solo se permiten correos de Gmail.")
        return email

