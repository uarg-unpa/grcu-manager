from django import forms
from accounts.models import Usuario  # Usuario está en accounts, no en usuarios
from roles.models import Rol
from django.core.exceptions import ValidationError

class UsuarioCrearForm(forms.ModelForm):
    roles = forms.ModelMultipleChoiceField(
        queryset=Rol.objects.filter(nombre__in=["Admin", "Desarrollador", "Stakeholder"]),  # Roles disponibles
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
        allowed_domains = ["gmail.com", "uarg.unpa.edu.ar"]
        if not any(email.lower().endswith(f"@{domain}") for domain in allowed_domains):
            raise ValidationError("Solo se permiten emails de los dominios: @gmail.com o @uarg.unpa.edu.ar")
        return email


class UsuarioEditarForm(forms.ModelForm):
    roles = forms.ModelMultipleChoiceField(
        queryset=Rol.objects.filter(nombre__in=["Admin", "Desarrollador", "Stakeholder"]),  # Roles disponibles
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
        allowed_domains = ["gmail.com", "uarg.unpa.edu.ar"]
        if not any(email.lower().endswith(f"@{domain}") for domain in allowed_domains):
            raise ValidationError("Solo se permiten emails de los dominios: @gmail.com o @uarg.unpa.edu.ar")
        return email

