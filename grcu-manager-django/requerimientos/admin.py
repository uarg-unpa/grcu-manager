from django.contrib import admin
from .models import Requerimiento, FuenteRequerimiento, CategoriaRequerimiento

@admin.register(Requerimiento)
class RequerimientoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "tipo", "estado", "proyecto", "fecha_creacion")
    search_fields = ("nombre", "descripcion")
    list_filter = ("tipo", "estado", "proyecto")


@admin.register(FuenteRequerimiento)
class FuenteRequerimientoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "proyecto", "es_predefinida", "veces_utilizada", "es_favorita", "fecha_creacion")
    search_fields = ("nombre", "proyecto__nombre")
    list_filter = ("es_predefinida", "es_favorita", "proyecto")
    readonly_fields = ("veces_utilizada", "fecha_creacion")


@admin.register(CategoriaRequerimiento)
class CategoriaRequerimientoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "proyecto", "es_predefinida", "veces_utilizada", "es_favorita", "fecha_creacion")
    search_fields = ("nombre", "proyecto__nombre")
    list_filter = ("es_predefinida", "es_favorita", "proyecto")
    readonly_fields = ("veces_utilizada", "fecha_creacion")
