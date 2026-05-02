"""Academic Calendar Models"""
from django.db import models

class AcademicEvent(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    event_type = models.CharField(max_length=50)  # exam, registration, lesson, holiday
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    created_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True)
    is_cancelled = models.BooleanField(default=False)
