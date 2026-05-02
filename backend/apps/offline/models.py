"""Offline App - Offline Sync Endpoints"""
import uuid
from django.db import models


class OfflineQueue(models.Model):
    """Offline Queue for sync operations"""
    
    OPERATION_TYPES = [
        ('attendance', 'Attendance'),
        ('assignment', 'Assignment Submission'),
        ('quiz', 'Quiz Attempt'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='offline_queue'
    )
    operation_type = models.CharField(max_length=20, choices=OPERATION_TYPES)
    payload = models.JSONField(default=dict)
    offline_token = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    synced_at = models.DateTimeField(null=True, blank=True)
    is_synced = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'offline_queue'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.operation_type} - {self.is_synced}"


class SyncStatus(models.Model):
    """Sync Status tracking"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='sync_status'
    )
    last_sync = models.DateTimeField(null=True, blank=True)
    pending_count = models.IntegerField(default=0)
    
    class Meta:
        db_table = 'sync_status'
    
    def __str__(self):
        return f"{self.user.email} - {self.last_sync}"