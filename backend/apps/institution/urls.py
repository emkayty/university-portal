"""Institution URL Configuration"""
from django.urls import path
from apps.institution import api

urlpatterns = [
    path('settings', api.get_settings, name='settings'),
    path('settings/update', api.update_settings, name='update_settings'),
    path('setup', api.setup_complete, name='setup'),
]