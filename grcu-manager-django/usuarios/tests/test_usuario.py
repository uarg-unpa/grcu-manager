import pytest
from accounts.models import Usuario
from usuarios.models import AccionUsuario

@pytest.mark.django_db
def test_accion_usuario_creation():
    # Crear usuario base
    user = Usuario.objects.create_user(email='usuario@demo.com', nombre='Usuario Demo', password='demopass123')
    assert user.email == 'usuario@demo.com'
    assert user.nombre == 'Usuario Demo'
    assert user.check_password('demopass123')
    assert user.is_active

    # Crear acción asociada
    accion = AccionUsuario.objects.create(usuario=user, accion='login')
    assert accion.usuario == user
    assert accion.accion == 'login'
    assert accion.fecha is not None
