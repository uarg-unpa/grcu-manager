import pytest
from accounts.models import Usuario
from auditoria.models import RegistroActividad

@pytest.mark.django_db
def test_registro_actividad_creation():
    # Crear usuario base
    user = Usuario.objects.create_user(email='usuario@demo.com', nombre='Usuario Demo', password='demopass123')
    assert user.email == 'usuario@demo.com'
    assert user.nombre == 'Usuario Demo'
    assert user.check_password('demopass123')
    assert user.is_active

    # Crear registro de actividad asociado (reemplaza AccionUsuario)
    registro = RegistroActividad.objects.create(
        usuario=user, 
        accion='LOGIN', 
        descripcion='Usuario inició sesión'
    )
    assert registro.usuario == user
    assert registro.accion == 'LOGIN'
    assert registro.fecha is not None
