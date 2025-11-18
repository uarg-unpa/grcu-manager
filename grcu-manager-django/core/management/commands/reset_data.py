from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.conf import settings
from django.db import connection

class Command(BaseCommand):
    help = "Elimina todos los datos de la base de datos y aplica migraciones. Funciona en PostgreSQL, SQLite y otros motores."

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Ejecuta el comando sin pedir confirmación interactiva',
        )

    def handle(self, *args, **options):
        if not settings.DEBUG:
            self.stdout.write(self.style.ERROR("❌ Este comando solo puede ejecutarse en modo DEBUG."))
            return

        force = options['force']
        
        if not force:
            self.stdout.write(self.style.WARNING("⚠️  Esto eliminará *todos* los datos de la base de datos."))

            confirm = input("¿Estás seguro de que querés continuar? (escribí 'SI' para continuar): ")
            if confirm != "SI":
                self.stdout.write(self.style.ERROR("Operación cancelada."))
                return

        engine = connection.settings_dict['ENGINE']
        self.stdout.write(f"Usando motor de base de datos: {engine}")

        try:
            if 'postgresql' in engine:
                self.stdout.write("🧨 PostgreSQL detectado: eliminando todas las tablas del esquema public...")
                with connection.cursor() as cursor:
                    cursor.execute("DROP SCHEMA public CASCADE;")
                    cursor.execute("CREATE SCHEMA public;")
                    self.stdout.write(self.style.SUCCESS("✅ Esquema eliminado y recreado."))
            
            elif 'sqlite' in engine:
                self.stdout.write("🗑️  SQLite detectado: eliminando archivo de base de datos...")
                db_name = connection.settings_dict['NAME']
                
                # Cerrar todas las conexiones
                connection.close()
                
                import os
                if os.path.exists(db_name):
                    os.remove(db_name)
                    self.stdout.write(self.style.SUCCESS(f"✅ Archivo eliminado: {db_name}"))
                else:
                    self.stdout.write(self.style.WARNING(f"⚠️  Archivo no encontrado: {db_name}"))
            
            else:
                self.stdout.write("🧹 Otro motor detectado: usando flush para limpiar todos los datos...")
                call_command("flush", "--no-input")

            self.stdout.write("🚀 Aplicando migraciones desde cero...")
            call_command("migrate", interactive=False, verbosity=2)
            
            self.stdout.write(self.style.SUCCESS("\n✅ Base de datos reseteada correctamente."))
            self.stdout.write(self.style.SUCCESS("💡 Ahora puedes ejecutar 'python manage.py createsuperuser' para crear un usuario administrador."))
            self.stdout.write(self.style.SUCCESS("💡 O usar 'python manage.py cargar_datos_demo' para cargar datos de prueba."))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Ocurrió un error: {e}"))
            import traceback
            self.stdout.write(self.style.ERROR(traceback.format_exc()))
