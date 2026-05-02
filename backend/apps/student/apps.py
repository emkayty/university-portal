"""App Configuration"""
from django.apps import AppConfig

class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.student'
    verbose_name = 'student'.title()
