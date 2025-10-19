from django.test import TestCase
from django.contrib.auth import get_user_model
from accounts.models import UsuarioManager

Usuario = get_user_model()

class UsuarioManagerTest(TestCase):
    def test_create_user(self):
        """Test que el manager crea usuarios correctamente con type hints"""
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
        """Test que el manager crea superusuarios correctamente"""
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
