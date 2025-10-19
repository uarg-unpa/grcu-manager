import pytest
from accounts.models import Usuario
from proyectos.models import Proyecto
from casos_de_uso.models import CasoDeUso

@pytest.mark.django_db
def test_caso_de_uso_creation():
    # Crear usuario y proyecto base
    user = Usuario.objects.create_user(email='caso@demo.com', nombre='Caso User', password='casopass123')
    proyecto = Proyecto.objects.create(nombre='Proyecto Caso', descripcion='desc')

    # Crear caso de uso
    caso = CasoDeUso.objects.create(
        nombre='Caso 1',
        descripcion='Desc caso',
        proyecto=proyecto,
        creado_por=user
    )
    assert caso.nombre == 'Caso 1'
    assert caso.proyecto == proyecto
    assert caso.creado_por == user
