from django.apps import AppConfig


class GruposConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'grupos'
    
    def ready(self):
        # Importar señales cuando la app esté lista
        import grupos.signals
