"""Offline Admin Configuration"""
from django.contrib import admin
from apps.offline.models import OfflineCache, SyncQueue


@admin.register(OfflineCache)
class OfflineCacheAdmin(admin.ModelAdmin):
    list_display = ['user', 'cache_type', 'created_at']
    list_filter = ['cache_type']


@admin.register(SyncQueue)
class SyncQueueAdmin(admin.ModelAdmin):
    list_display = ['user', 'operation', 'status', 'created_at']
    list_filter = ['status']
    raw_id_fields = ['user']
