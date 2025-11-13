"""
Tests unitarios para el modelo Usuario y su manager personalizado.

Este módulo contiene pruebas para verificar el correcto funcionamiento
del UsuarioManager y el modelo Usuario, incluyendo la creación de usuarios
regulares y superusuarios con type hints.

Clases:
    UsuarioManagerTest: Tests para el manager personalizado de Usuario.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from accounts.models import UsuarioManager

Usuario = get_user_model()


class UsuarioManagerTest(TestCase):
    """
    Suite de tests para el UsuarioManager personalizado.

    Verifica que el manager crea correctamente usuarios regulares y
    superusuarios con los campos y permisos adecuados.
    """

    def test_create_user(self):
        """
        Test que el manager crea usuarios correctamente con type hints.

        Verifica que:
        - El email se guarda correctamente.
        - El nombre se asigna correctamente.
        - La contraseña se hashea (no se guarda en texto plano).
        - Los flags is_staff e is_superuser son False.
        """
        user = Usuario.objects.create_user(
            email='test@example.com',
            nombre='Test User',
            password='testpass123'
        )
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.nombre, 'Test User')
        self.assertTrue(user.check_password('testpass123'))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        """
        Test que el manager crea superusuarios correctamente.

        Verifica que:
        - El email se guarda correctamente.
        - El nombre se asigna correctamente.
        - La contraseña se hashea correctamente.
        - Los flags is_staff e is_superuser son True.
        """
        superuser = Usuario.objects.create_superuser(
            email='admin@example.com',
            nombre='Admin User',
            password='adminpass123'
        )
        self.assertEqual(superuser.email, 'admin@example.com')
        self.assertEqual(superuser.nombre, 'Admin User')
        self.assertTrue(superuser.check_password('adminpass123'))
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
