from django.apps import AppConfig

class SbappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sbapp'

    def ready(self):
        import sbapp.signals  # Import the signals module