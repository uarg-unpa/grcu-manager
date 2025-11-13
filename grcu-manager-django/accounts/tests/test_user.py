"""
Tests de creación de usuarios usando pytest.

Este módulo contiene pruebas con pytest para verificar la creación
correcta de usuarios mediante el UsuarioManager personalizado.

Tests:
    - test_user_creation: Verifica la creación de un usuario regular.
"""

import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
def test_user_creation():
    """
    Test de creación de usuario con pytest.

    Verifica que:
    - El usuario se crea correctamente con email como identificador.
    - El nombre se asigna correctamente.
    - La contraseña se hashea correctamente.
    - El usuario está activo por defecto.
    """
    user = User.objects.create_user(
        email='test@demo.com',
        nombre='Test User',
        password='testpass123'
    )
    assert user.email == 'test@demo.com'
    assert user.nombre == 'Test User'
    assert user.check_password('testpass123')
    assert user.is_active
