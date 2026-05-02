"""App Configuration"""
from django.apps import AppConfig

class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.communication'
    verbose_name = 'communication'.title()
