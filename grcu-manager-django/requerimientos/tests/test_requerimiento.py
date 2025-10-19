import pytest
from accounts.models import Usuario
from proyectos.models import Proyecto
from requerimientos.models import Requerimiento

@pytest.mark.django_db
def test_requerimiento_creation():
    # Crear usuario y proyecto base
    user = Usuario.objects.create_user(email='req@demo.com', nombre='Req User', password='reqpass123')
    proyecto = Proyecto.objects.create(nombre='Proyecto Test', descripcion='desc')

    # Crear requerimiento
    req = Requerimiento.objects.create(
        nombre='Requerimiento 1',
        descripcion='Desc de prueba',
        tipo='FUNCIONAL',
        estado='PENDIENTE',
        proyecto=proyecto,
        creado_por=user
    )
    assert req.nombre == 'Requerimiento 1'
    assert req.proyecto == proyecto
    assert req.creado_por == user
    assert req.estado == 'PENDIENTE'
