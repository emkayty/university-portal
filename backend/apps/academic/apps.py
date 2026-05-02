"""
Academic App Configuration
========================
Academic management module for universities.
"""
from django.apps import AppConfig


class AcademicConfig(AppConfig):
    """Academic application configuration."""
    
    name = 'apps.academic'
    verbose_name = 'Academic Management'
    label = 'academic'
    
    # Menu configuration
    menu_icon = 'Building'
    menu_order = 2
    menu_category = 'academic'
    
    def ready(self):
        """Import signals when app is ready."""
        pass