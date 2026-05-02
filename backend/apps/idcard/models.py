"""ID Card Models"""
from django.db import models

class IDCard(models.Model):
    student = models.OneToOneField('student.StudentProfile', on_delete=models.CASCADE)
    card_number = models.CharField(max_length=20, unique=True)
    issue_date = models.DateField(auto_now_add=True)
    expiry_date = models.DateField()
    status = models.CharField(max_length=20, default='active')
    barcode = models.CharField(max_length=50, blank=True)
