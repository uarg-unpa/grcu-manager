from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta

from auditoria.models import RegistroActividad
from accounts.models import Usuario
from roles.models import Rol


class AuditoriaViewsTestCase(TestCase):
    """Pruebas para las vistas de auditoría"""

    def setUp(self):
        """Configurar datos de prueba"""
        self.client = Client()

        # Obtener o crear rol de admin
        self.rol_admin, _ = Rol.objects.get_or_create(nombre=Rol.ADMIN)

        # Crear usuario admin
        self.admin_user = Usuario.objects.create_user(
            email="admin@test.com",
            nombre="Admin User",
            password="testpass123"
        )
        self.admin_user.roles.add(self.rol_admin)

        # Crear usuario normal
        self.normal_user = Usuario.objects.create_user(
            email="user@test.com",
            nombre="Normal User",
            password="testpass123"
        )

        # Crear algunas actividades de prueba
        RegistroActividad.objects.create(
            usuario=self.admin_user,
            accion='LOGIN',
            descripcion='Inicio de sesión exitoso',
            ip_address='192.168.1.1'
        )

        RegistroActividad.objects.create(
            usuario=self.normal_user,
            accion='CREATE_USER',
            descripcion='Creación de nuevo usuario',
            ip_address='192.168.1.2'
        )

    def test_admin_dashboard_access_denied_for_normal_user(self):
        """Verificar que usuarios normales no puedan acceder al dashboard de auditoría"""
        self.client.login(email='user@test.com', password='testpass123')
        response = self.client.get(reverse('auditoria:admin_dashboard'))
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_admin_dashboard_access_granted_for_admin(self):
        """Verificar que administradores puedan acceder al dashboard de auditoría"""
        self.client.login(email='admin@test.com', password='testpass123')
        response = self.client.get(reverse('auditoria:admin_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Auditoría del Sistema')

    def test_admin_dashboard_contains_metrics(self):
        """Verificar que el dashboard contenga métricas básicas"""
        self.client.login(email='admin@test.com', password='testpass123')
        response = self.client.get(reverse('auditoria:admin_dashboard'))

        # Verificar métricas principales
        self.assertContains(response, 'actividades totales')
        self.assertContains(response, 'Actividades encontradas')

        # Verificar que contenga datos del gráfico
        self.assertContains(response, 'auditoriaChartData')

    def test_admin_dashboard_filtering(self):
        """Verificar que los filtros funcionen correctamente"""
        self.client.login(email='admin@test.com', password='testpass123')

        # Filtrar por acción LOGIN
        response = self.client.get(reverse('auditoria:admin_dashboard'), {'accion': 'LOGIN'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Inicio de sesión exitoso')

        # Filtrar por usuario
        response = self.client.get(reverse('auditoria:admin_dashboard'),
                                 {'usuario': str(self.admin_user.id)})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Admin User')

    def test_actividad_detalle_view(self):
        """Verificar la vista de detalle de actividad"""
        actividad = RegistroActividad.objects.filter(accion='LOGIN').first()

        self.client.login(email='admin@test.com', password='testpass123')
        response = self.client.get(reverse('auditoria:actividad_detalle',
                                         kwargs={'actividad_id': actividad.id}))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Detalle de Actividad')
        self.assertContains(response, 'Inicio de sesión exitoso')
        self.assertContains(response, '192.168.1.1')

    def test_actividad_detalle_access_denied_for_normal_user(self):
        """Verificar que usuarios normales no puedan ver detalles de actividades"""
        actividad = RegistroActividad.objects.first()

        self.client.login(email='user@test.com', password='testpass123')
        response = self.client.get(reverse('auditoria:actividad_detalle',
                                         kwargs={'actividad_id': actividad.id}))
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_pagination(self):
        """Verificar que la paginación funcione correctamente"""
        # Crear más actividades para probar paginación
        for i in range(30):
            RegistroActividad.objects.create(
                usuario=self.admin_user,
                accion='LOGIN',
                descripcion=f'Actividad de prueba {i}',
                ip_address='192.168.1.100'
            )

        self.client.login(email='admin@test.com', password='testpass123')

        # Página 1
        response = self.client.get(reverse('auditoria:admin_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'pagination')

        # Página 2
        response = self.client.get(reverse('auditoria:admin_dashboard'), {'page': '2'})
        self.assertEqual(response.status_code, 200)


class RegistroActividadModelTestCase(TestCase):
    """Pruebas para el modelo RegistroActividad"""

    def setUp(self):
        self.user = Usuario.objects.create_user(
            email="test@test.com",
            nombre="Test User",
            password="testpass123"
        )

    def test_registro_actividad_creation(self):
        """Verificar creación de registro de actividad"""
        actividad = RegistroActividad.objects.create(
            usuario=self.user,
            accion='LOGIN',
            descripcion='Prueba de login',
            ip_address='127.0.0.1'
        )

        self.assertEqual(actividad.usuario, self.user)
        self.assertEqual(actividad.accion, 'LOGIN')
        self.assertEqual(actividad.descripcion, 'Prueba de login')
        self.assertEqual(actividad.ip_address, '127.0.0.1')
        self.assertIsNotNone(actividad.fecha)

    def test_registro_actividad_str(self):
        """Verificar representación string del modelo"""
        actividad = RegistroActividad.objects.create(
            usuario=self.user,
            accion='LOGIN',
            descripcion='Prueba de login'
        )

        expected_str = f"LOGIN - {self.user.nombre} - {actividad.fecha.strftime('%Y-%m-%d %H:%M:%S')}"
        self.assertEqual(str(actividad), expected_str)

    def test_accion_choices(self):
        """Verificar que las opciones de acción estén definidas"""
        choices = dict(RegistroActividad.ACCION_CHOICES)
        self.assertIn('LOGIN', choices)
        self.assertIn('LOGOUT', choices)
        self.assertIn('CREATE_USER', choices)
        self.assertEqual(choices['LOGIN'], 'Inicio de sesión')
        self.assertEqual(choices['LOGOUT'], 'Cierre de sesión')
