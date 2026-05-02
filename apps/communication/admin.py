"""Communication Admin Configuration"""
from django.contrib import admin
from apps.communication.models import Announcement, Notification, NotificationTemplate


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['title', 'priority', 'target_audience', 'created_at']
    list_filter = ['priority', 'target_audience']


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'is_read', 'created_at']
    list_filter = ['is_read']
    raw_id_fields = ['user']


@admin.register(NotificationTemplate)
class NotificationTemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'channel']
    list_filter = ['channel']
