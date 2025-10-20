from django.urls import path
from . import views

app_name = "proyectos"

urlpatterns = [
    path("", views.lista_proyectos, name="lista_proyectos"),
    path("crear/", views.crear_proyecto, name="crear_proyecto"),
    path("editar/<int:proyecto_id>/", views.editar_proyecto, name="editar_proyecto"),
    path("eliminar/<int:proyecto_id>/", views.eliminar_proyecto, name="eliminar_proyecto"),
    path("<int:proyecto_id>/metodologia/", views.asignar_metodologia, name="asignar_metodologia"),
    path("<int:proyecto_id>/matriz/", views.matriz_trazabilidad, name="matriz_trazabilidad"),
    path("<int:proyecto_id>/matriz/exportar/<str:formato>/", views.exportar_matriz, name="exportar_matriz"),
    path("<int:proyecto_id>/reportes/", views.proyecto_reportes, name="proyecto_reportes"),
    path("<int:proyecto_id>/integrantes/", views.gestionar_integrantes, name="gestionar_integrantes"),
    path("<int:proyecto_id>/detail/", views.proyecto_detail_admin, name="proyecto_detail_admin"),
]
