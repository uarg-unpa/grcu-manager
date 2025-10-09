from django.contrib import admin
from .models import Requerimiento

@admin.register(Requerimiento)
class RequerimientoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "tipo", "estado", "proyecto", "fecha_creacion")
    search_fields = ("nombre", "descripcion")
    list_filter = ("tipo", "estado", "proyecto")
