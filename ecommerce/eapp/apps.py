from django.apps import AppConfig



class EappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'eapp'
    
    def ready(self):
        import eapp.signals  
 