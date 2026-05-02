"""App Configuration"""
from django.apps import AppConfig

class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.finance'
    verbose_name = 'finance'.title()
