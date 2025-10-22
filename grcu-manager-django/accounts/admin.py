from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    model = Usuario

    ordering = ['email']
    list_display = ['email', 'nombre']
    list_filter = ['roles'] 

    fieldsets = (
        (None, {'fields': ('email', 'nombre', 'password', 'roles')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'nombre', 'password1', 'password2', 'roles', 'is_staff', 'is_active')}
        ),
    )

    search_fields = ['email', 'nombre']
