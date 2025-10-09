from django.contrib import admin
from .models import CasoDeUso, DetalleCasoDeUsoTradicional, DetalleCasoDeUsoAgil

@admin.register(CasoDeUso)
class CasoDeUsoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "proyecto", "fecha_creacion")
    search_fields = ("nombre", "descripcion")
    list_filter = ("proyecto",)

@admin.register(DetalleCasoDeUsoTradicional)
class DetalleCasoDeUsoTradicionalAdmin(admin.ModelAdmin):
    list_display = ("caso_de_uso_padre", "actor_principal")

@admin.register(DetalleCasoDeUsoAgil)
class DetalleCasoDeUsoAgilAdmin(admin.ModelAdmin):
    list_display = ("caso_de_uso_padre", "responsable")
