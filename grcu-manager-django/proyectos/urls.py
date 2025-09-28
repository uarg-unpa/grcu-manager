from django.urls import path
from . import views

app_name = "proyectos"

urlpatterns = [
    path("", views.lista_proyectos, name="lista_proyectos"),
    path("crear/", views.crear_proyecto, name="crear_proyecto"),
    path("editar/<int:proyecto_id>/", views.editar_proyecto, name="editar_proyecto"),
    path("eliminar/<int:proyecto_id>/", views.eliminar_proyecto, name="eliminar_proyecto"),
]
