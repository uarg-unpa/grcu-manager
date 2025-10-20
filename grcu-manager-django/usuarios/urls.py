from django.urls import path
from .views import lista_usuarios, crear_usuario, editar_usuario, eliminar_usuario, buscar_usuarios_ajax

app_name = "usuarios"

urlpatterns = [
    path("", lista_usuarios, name="lista"),                         # Lista de usuarios
    path("crear/", crear_usuario, name="crear"),                    # Crear usuario
    path("editar/<int:pk>/", editar_usuario, name="editar"),        # Editar usuario por ID
    path("eliminar/<int:pk>/", eliminar_usuario, name="eliminar"),  # Eliminar usuario por ID
    path("buscar/", buscar_usuarios_ajax, name="buscar_ajax"),      # Búsqueda AJAX
]
