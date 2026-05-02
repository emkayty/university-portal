"""Reports App - Analytics & Accreditation Models"""
import uuid
from django.db import models


class AccreditationReport(models.Model):
    """Accreditation Report"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    report_type = models.CharField(max_length=50)
    data = models.JSONField(default=dict)
    generated_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'accreditation_reports'
        ordering = ['-generated_at']
    
    def __str__(self):
        return f"{self.name} - {self.generated_at}"