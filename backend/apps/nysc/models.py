"""NYSC Models - National Youth Service Corps"""
from django.db import models

class NYSCProfile(models.Model):
    """Student NYSC data"""
    student = models.ForeignKey('student.StudentProfile', on_delete=models.CASCADE)
    call_up_number = models.CharField(max_length=20, unique=True, null=True)
    batch = models.CharField(max_length=10, blank=True)
    year = models.IntegerField()
    state_code = models.CharField(max_length=10, blank=True)
    lga = models.CharField(max_length=50, blank=True)
    ppa = models.CharField(max_length=100, blank=True)  # Place of Primary Assignment
    ppa_address = models.TextField(blank=True)
    service_start = models.DateField(null=True, blank=True)
    service_end = models.DateField(null=True, blank=True)
    certificate_number = models.CharField(max_length=20, blank=True)
    status = models.CharField(max_length=20, default='pending')  # pending, deployed, ongoing, completed

class NYSCBatch(models.Model):
    """NYSC batch management"""
    batch = models.CharField(max_length=10)
    year = models.IntegerField()
    stream = models.CharField(max_length=5)
    start_date = models.DateField()
    end_date = models.DateField()
    registration_deadline = models.DateField()
    is_active = models.BooleanField(default=True)
