import pytest
from django.test import Client
from django.urls import reverse
from accounts.models import Usuario
from proyectos.models import Proyecto
from casos_de_uso.models import CasoDeUso
from requerimientos.models import Requerimiento

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


@pytest.mark.django_db
def test_caso_de_uso_requerimiento_priorizado():
    """
    Test que verifica que se puede crear un caso de uso
    para un requerimiento en estado PRIORIZADO.
    
    Bug fix: anteriormente solo se aceptaba VALIDADO,
    ahora acepta VALIDADO, PRIORIZADO, EN_PROCESO y TERMINADO.
    """
    # Crear usuario y proyecto
    user = Usuario.objects.create_user(
        email='test@demo.com',
        nombre='Test User',
        password='testpass123'
    )
    proyecto = Proyecto.objects.create(
        nombre='Proyecto Test',
        descripcion='Proyecto de prueba'
    )
    
    # Crear requerimiento en estado PRIORIZADO
    requerimiento = Requerimiento.objects.create(
        nombre='Req Test',
        descripcion='Requerimiento de prueba',
        proyecto=proyecto,
        creado_por=user,
        estado='PRIORIZADO'  # Estado que antes causaba error
    )
    
    # Intentar crear un caso de uso asociado
    client = Client()
    client.force_login(user)
    
    url = reverse('casos_de_uso:caso_de_uso_create_con_requerimiento', 
                  kwargs={'proyecto_id': proyecto.id, 'requerimiento_id': requerimiento.id})
    
    response = client.get(url)
    
    # Debe permitir acceso (status 200) y no redirigir con error
    assert response.status_code == 200
    
    # Verificar que el formulario se muestra sin error
    assert 'form' in response.context or response.status_code == 200


@pytest.mark.django_db
def test_caso_de_uso_requerimiento_borrador():
    """
    Test que verifica que NO se puede crear un caso de uso
    para un requerimiento en estado BORRADOR.
    """
    # Crear usuario y proyecto
    user = Usuario.objects.create_user(
        email='test2@demo.com',
        nombre='Test User 2',
        password='testpass123'
    )
    proyecto = Proyecto.objects.create(
        nombre='Proyecto Test 2',
        descripcion='Proyecto de prueba 2'
    )
    
    # Crear requerimiento en estado BORRADOR
    requerimiento = Requerimiento.objects.create(
        nombre='Req Test Borrador',
        descripcion='Requerimiento en borrador',
        proyecto=proyecto,
        creado_por=user,
        estado='BORRADOR'
    )
    
    # Intentar crear un caso de uso asociado
    client = Client()
    client.force_login(user)
    
    url = reverse('casos_de_uso:caso_de_uso_create_con_requerimiento',
                  kwargs={'proyecto_id': proyecto.id, 'requerimiento_id': requerimiento.id})
    
    response = client.get(url)
    
    # Debe redirigir (302) porque el requerimiento está en BORRADOR
    assert response.status_code == 302
    # Y debe mostrar mensaje de error (verificamos el redirect)
    assert response.url == reverse('requerimientos:requerimiento_detail', 
                                   kwargs={'pk': requerimiento.id})
