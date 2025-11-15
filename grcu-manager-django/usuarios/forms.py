from django import forms
from accounts.models import Usuario  # Usuario está en accounts, no en usuarios
from roles.models import Rol
from django.core.exceptions import ValidationError

class UsuarioCrearForm(forms.ModelForm):
    roles = forms.ModelChoiceField(
        queryset=Rol.objects.filter(nombre__in=["Admin", "Desarrollador", "Stakeholder"]),  # Roles disponibles
        widget=forms.RadioSelect,
        required=False,
        empty_label="Sin rol asignado"
    )
    password = forms.CharField(widget=forms.HiddenInput(), required=False)  # opcional

    class Meta:
        model = Usuario
        fields = ["email", "roles", "is_active"]

    def save(self, commit=True):
        user = super().save(commit=False)

        if commit:
            user.save()  # Guardar primero el usuario

            # Después de guardar, manejar la asignación de roles
            selected_rol = self.cleaned_data.get('roles')
            if selected_rol:
                # Asignar el rol seleccionado
                user.roles.set([selected_rol])
            # Si no se seleccionó ningún rol, no hacer nada (ya que es un usuario nuevo)

        return user

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not email:
            raise ValidationError("El email es obligatorio.")
        allowed_domains = ["gmail.com", "uarg.unpa.edu.ar"]
        if not any(email.lower().endswith(f"@{domain}") for domain in allowed_domains):
            raise ValidationError("Solo se permiten emails de los dominios: @gmail.com o @uarg.unpa.edu.ar")
        return email


class UsuarioEditarForm(forms.ModelForm):
    roles = forms.ModelChoiceField(
        queryset=Rol.objects.filter(nombre__in=["Admin", "Desarrollador", "Stakeholder"]),  # Roles disponibles
        widget=forms.RadioSelect,
        required=False,
        empty_label="Sin rol asignado"
    )

    class Meta:
        model = Usuario
        fields = ["email", "roles", "is_active"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Si el usuario ya tiene roles, seleccionar el primero
        if self.instance and self.instance.pk and self.instance.roles.exists():
            self.initial['roles'] = self.instance.roles.first().pk

    def save(self, commit=True):
        user = super().save(commit=False)

        # Manejar la asignación de roles
        selected_rol = self.cleaned_data.get('roles')
        if selected_rol:
            # Asignar el rol seleccionado (reemplaza cualquier rol anterior)
            user.roles.set([selected_rol])
        else:
            # Si no se seleccionó ningún rol, quitar todos los roles
            user.roles.clear()

        if commit:
            user.save()
            # No necesitamos save_m2m() porque ya manejamos la relación manualmente

        return user

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not email:
            raise ValidationError("El email es obligatorio.")
        allowed_domains = ["gmail.com", "uarg.unpa.edu.ar"]
        if not any(email.lower().endswith(f"@{domain}") for domain in allowed_domains):
            raise ValidationError("Solo se permiten emails de los dominios: @gmail.com o @uarg.unpa.edu.ar")
        return email

