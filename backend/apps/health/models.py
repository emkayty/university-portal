"""Health Models - Medical Centre"""
from django.db import models

class HealthRecord(models.Model):
    student = models.ForeignKey('student.StudentProfile', on_delete=models.CASCADE)
    visit_date = models.DateTimeField(auto_now_add=True)
    symptoms = models.TextField()
    diagnosis = models.TextField(blank=True)
    treatment = models.TextField(blank=True)
    prescribed_meds = models.TextField(blank=True)
    doctor = models.CharField(max_length=100, blank=True)

class MedicalRequest(models.Model):
    student = models.ForeignKey('student.StudentProfile', on_delete=models.CASCADE)
    session = models.ForeignKey('academic.AcademicSession', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, default='pending')
    clearance_status = models.BooleanField(default=False)

class PharmacyItem(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.IntegerField(default=0)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    expiry_date = models.DateField(null=True, blank=True)
