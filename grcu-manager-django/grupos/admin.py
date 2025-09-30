from django.contrib import admin
from .models import Grupo

@admin.register(Grupo)
class GrupoAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre")
    search_fields = ("nombre",)
    filter_horizontal = ("integrantes",)
