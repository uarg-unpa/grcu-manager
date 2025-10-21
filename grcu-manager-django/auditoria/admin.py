from django.contrib import admin
from .models import RegistroActividad


@admin.register(RegistroActividad)
class RegistroActividadAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'accion', 'descripcion_corta', 'ip_address', 'fecha')
    list_filter = ('accion', 'fecha')
    search_fields = ('usuario__email', 'usuario__nombre', 'descripcion')
    readonly_fields = ('usuario', 'accion', 'descripcion', 'detalles', 'ip_address', 'user_agent', 'fecha')
    date_hierarchy = 'fecha'
    
    @admin.display(description='Descripción')
    def descripcion_corta(self, obj):
        return obj.descripcion[:50] + '...' if len(obj.descripcion) > 50 else obj.descripcion
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

