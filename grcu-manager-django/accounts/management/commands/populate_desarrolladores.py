"""
Comando de gestión Django para poblar la base de datos con usuarios desarrolladores.

Este script crea 100 usuarios de prueba con el rol de Desarrollador,
generando nombres y emails aleatorios para facilitar el testing y
desarrollo del sistema.

Uso:
    python manage.py populate_desarrolladores

Clases:
    Command: Comando personalizado de Django para crear usuarios masivamente.
"""

from django.core.management.base import BaseCommand
from accounts.models import Usuario
from roles.models import Rol
import random
import string


class Command(BaseCommand):
    """
    Comando para crear 100 usuarios desarrolladores de prueba.

    Genera usuarios con nombres y apellidos realistas en español,
    emails únicos en el dominio @visitante.test, y asigna el rol
    de Desarrollador a cada uno.

    Attributes:
        help (str): Descripción del comando mostrada en --help.
    """

    help = 'Crea 100 usuarios desarrolladores para poblar la base de datos'

    def handle(self, *args, **options):
        """
        Método principal que ejecuta la creación masiva de usuarios.

        Proceso:
        1. Obtiene o crea el rol Desarrollador.
        2. Itera 100 veces generando usuarios aleatorios.
        3. Asegura unicidad de emails.
        4. Asigna rol y contraseña por defecto.
        5. Reporta progreso cada 10 usuarios.

        Args:
            *args: Argumentos posicionales (no utilizados).
            **options: Opciones del comando (no utilizadas).
        """
        # Obtener o crear el rol Desarrollador
        desarrollador_role, created = Rol.objects.get_or_create(
            nombre=Rol.DESARROLLADOR,
            defaults={
                "color": "#3498db",
                "icono_url": "/static/roles/icons/developer.png"
            }
        )

        if created:
            self.stdout.write(
                self.style.SUCCESS('Rol "Desarrollador" creado')
            )

        # Nombres comunes para generar usuarios realistas
        nombres = [
            'Ana', 'Carlos', 'María', 'José', 'Laura', 'Miguel', 'Carmen',
            'David', 'Isabel', 'Francisco', 'Pilar', 'Antonio', 'Teresa',
            'Juan', 'Cristina', 'Manuel', 'Mónica', 'Ángel', 'Dolores',
            'Javier', 'Lucía', 'Fernando', 'Mercedes', 'Pablo', 'Rosa',
            'Sergio', 'Raquel', 'Diego', 'Elena', 'Adrián', 'Silvia',
            'Alberto', 'Patricia', 'Raúl', 'Beatriz', 'Rubén', 'Inés',
            'Iván', 'Nuria', 'Óscar', 'Alicia', 'Roberto', 'Sonia',
            'Gonzalo', 'Eva', 'Hugo', 'Irene', 'Mario', 'Lourdes', 'Víctor',
            'Marta', 'Enrique', 'Natalia', 'Salvador', 'Ángela', 'Guillermo',
            'Claudia', 'Emilio', 'Sonia', 'Felipe', 'Lorena', 'Jesús',
            'Marina', 'Rafael', 'Teresa', 'Vicente', 'Cristina', 'Andrés',
            'Mónica', 'Tomás', 'Pilar', 'Eduardo', 'Mercedes', 'Ramón',
            'Rosa', 'Santiago', 'Beatriz', 'Agustín', 'Silvia', 'Julio',
            'Natalia', 'Joaquín', 'Eva', 'Federico', 'Irene', 'Luis',
            'Lourdes', 'Marcos', 'Marta', 'Hugo', 'Ángela', 'Adriana',
            'Roberto', 'Valeria', 'Gonzalo', 'Camila', 'Leonardo', 'Sofía',
            'Mateo', 'Valentina', 'Diego', 'Isabella'
        ]

        apellidos = [
            'García', 'Rodríguez', 'González', 'Fernández', 'López',
            'Martínez', 'Sánchez', 'Pérez', 'Martín', 'Ruiz', 'Hernández',
            'Jiménez', 'Díaz', 'Moreno', 'Álvarez', 'Muñoz', 'Romero',
            'Navarro', 'Torres', 'Gil', 'Ramírez', 'Serrano', 'Blanco',
            'Suárez', 'Molina', 'Morales', 'Ortega', 'Delgado', 'Castro',
            'Ortiz', 'Rubio', 'Sanz', 'Iglesias', 'Gutiérrez', 'Santana',
            'Vargas', 'Herrera', 'Medina', 'Cortés', 'Castillo', 'Santos',
            'Arias', 'Flores', 'Cabrera', 'Campos', 'Vega', 'Santiago',
            'Núñez', 'Reyes', 'Fuentes', 'Carrasco', 'Diez', 'Caballero',
            'Rivas', 'León', 'Vázquez', 'Gómez', 'Mendoza', 'Santiago',
            'Silva', 'Marín', 'Prieto', 'Lorenzo', 'Vidal', 'Benítez',
            'Santiago', 'Ramos', 'Hidalgo', 'Ibáñez', 'Ferrer', 'Duran',
            'Santiago', 'Vicente', 'Herrero', 'Domínguez', 'Guerrero',
            'Santiago', 'Crespo', 'Luna', 'Pastor', 'Velasco', 'Moya',
            'Santiago', 'Bravo', 'Rivera', 'Aguilar', 'Santiago', 'Soler',
            'Parra', 'Santiago', 'Esteban', 'Rojas', 'Santiago', 'Pascual',
            'Santiago'
        ]

        usuarios_creados = 0

        for i in range(100):
            # Generar nombre completo aleatorio
            nombre = f"{random.choice(nombres)} {random.choice(apellidos)}"

            # Generar email único
            # Usar un dominio genérico para evitar conflictos con emails reales
            email_base = nombre.lower().replace(' ', '.') \
                .replace('á', 'a').replace('é', 'e').replace('í', 'i') \
                .replace('ó', 'o').replace('ú', 'u').replace('ñ', 'n')
            
            # Añadir un número aleatorio para asegurar unicidad
            numero = random.randint(100, 999)
            email = f"{email_base}{numero}@visitante.test"

            # Verificar que el email no exista
            if Usuario.objects.filter(email=email).exists():
                # Si existe, añadir otro número
                email = (
                    f"{email_base}{numero}"
                    f"{random.randint(10, 99)}@visitante.test"
                )

            try:
                # Crear usuario directamente
                usuario = Usuario(
                    email=email,
                    nombre=nombre,
                    is_active=True
                )
                usuario.set_password('password123')
                usuario.save()

                # Asignar rol desarrollador
                usuario.roles.add(desarrollador_role)

                usuarios_creados += 1

                if usuarios_creados % 10 == 0:
                    self.stdout.write(
                        f'Creados {usuarios_creados} usuarios...'
                    )

            except Exception as e:
                self.stdout.write(
                    self.style.WARNING(
                        f'Error creando usuario {email}: {str(e)}'
                    )
                )
                continue

        self.stdout.write(
            self.style.SUCCESS(
                f'Se crearon exitosamente {usuarios_creados} '
                f'usuarios desarrolladores'
            )
        )

        # Obtener o crear el rol Desarrollador
        desarrollador_role, created = Rol.objects.get_or_create(
            nombre=Rol.DESARROLLADOR,
            defaults={"color": "#3498db", "icono_url": "/static/roles/icons/developer.png"}
        )

        if created:
            self.stdout.write(
                self.style.SUCCESS(f'Rol "Desarrollador" creado')
            )

        # Nombres comunes para generar usuarios realistas
        nombres = [
            'Ana', 'Carlos', 'María', 'José', 'Laura', 'Miguel', 'Carmen', 'David',
            'Isabel', 'Francisco', 'Pilar', 'Antonio', 'Teresa', 'Juan', 'Cristina',
            'Manuel', 'Mónica', 'Ángel', 'Dolores', 'Javier', 'Lucía', 'Fernando',
            'Mercedes', 'Pablo', 'Rosa', 'Sergio', 'Raquel', 'Diego', 'Elena',
            'Adrián', 'Silvia', 'Alberto', 'Patricia', 'Raúl', 'Beatriz', 'Rubén',
            'Inés', 'Iván', 'Nuria', 'Óscar', 'Alicia', 'Roberto', 'Sonia',
            'Gonzalo', 'Eva', 'Hugo', 'Irene', 'Mario', 'Lourdes', 'Víctor',
            'Marta', 'Enrique', 'Natalia', 'Salvador', 'Ángela', 'Guillermo',
            'Claudia', 'Emilio', 'Sonia', 'Felipe', 'Lorena', 'Jesús', 'Marina',
            'Rafael', 'Teresa', 'Vicente', 'Cristina', 'Andrés', 'Mónica',
            'Tomás', 'Pilar', 'Eduardo', 'Mercedes', 'Ramón', 'Rosa', 'Santiago',
            'Beatriz', 'Agustín', 'Silvia', 'Julio', 'Natalia', 'Joaquín', 'Eva',
            'Federico', 'Irene', 'Luis', 'Lourdes', 'Marcos', 'Marta', 'Hugo',
            'Ángela', 'Adriana', 'Roberto', 'Valeria', 'Gonzalo', 'Camila',
            'Leonardo', 'Sofía', 'Mateo', 'Valentina', 'Diego', 'Isabella'
        ]

        apellidos = [
            'García', 'Rodríguez', 'González', 'Fernández', 'López', 'Martínez',
            'Sánchez', 'Pérez', 'Martín', 'Ruiz', 'Hernández', 'Jiménez', 'Díaz',
            'Moreno', 'Álvarez', 'Muñoz', 'Romero', 'Navarro', 'Torres', 'Gil',
            'Ramírez', 'Serrano', 'Blanco', 'Suárez', 'Molina', 'Morales', 'Ortega',
            'Delgado', 'Castro', 'Ortiz', 'Rubio', 'Sanz', 'Iglesias', 'Gutiérrez',
            'Santana', 'Vargas', 'Herrera', 'Medina', 'Cortés', 'Castillo', 'Santos',
            'Arias', 'Flores', 'Cabrera', 'Campos', 'Vega', 'Santiago', 'Núñez',
            'Reyes', 'Fuentes', 'Carrasco', 'Diez', 'Caballero', 'Rivas', 'León',
            'Vázquez', 'Gómez', 'Mendoza', 'Santiago', 'Silva', 'Marín', 'Prieto',
            'Lorenzo', 'Vidal', 'Benítez', 'Santiago', 'Ramos', 'Hidalgo', 'Ibáñez',
            'Ferrer', 'Duran', 'Santiago', 'Vicente', 'Herrero', 'Domínguez',
            'Guerrero', 'Santiago', 'Crespo', 'Luna', 'Pastor', 'Velasco', 'Moya',
            'Santiago', 'Bravo', 'Rivera', 'Aguilar', 'Santiago', 'Soler', 'Parra',
            'Santiago', 'Esteban', 'Rojas', 'Santiago', 'Pascual', 'Santiago'
        ]

        usuarios_creados = 0

        for i in range(100):
            # Generar nombre completo aleatorio
            nombre = f"{random.choice(nombres)} {random.choice(apellidos)}"

            # Generar email único
            # Usar un dominio genérico para evitar conflictos con emails reales
            email_base = f"{nombre.lower().replace(' ', '.').replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u').replace('ñ', 'n')}"
            # Añadir un número aleatorio para asegurar unicidad
            numero = random.randint(100, 999)
            email = f"{email_base}{numero}@visitante.test"

            # Verificar que el email no exista
            if Usuario.objects.filter(email=email).exists():
                # Si existe, añadir otro número
                email = f"{email_base}{numero}{random.randint(10, 99)}@visitante.test"

            try:
                # Crear usuario directamente
                usuario = Usuario(
                    email=email,
                    nombre=nombre,
                    is_active=True
                )
                usuario.set_password('password123')
                usuario.save()

                # Asignar rol desarrollador
                usuario.roles.add(desarrollador_role)

                usuarios_creados += 1

                if usuarios_creados % 10 == 0:
                    self.stdout.write(f'Creados {usuarios_creados} usuarios...')

            except Exception as e:
                self.stdout.write(
                    self.style.WARNING(f'Error creando usuario {email}: {str(e)}')
                )
                continue

        self.stdout.write(
            self.style.SUCCESS(f'Se crearon exitosamente {usuarios_creados} usuarios desarrolladores')
        )