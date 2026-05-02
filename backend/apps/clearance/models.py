"""Graduation Clearance Models"""
from django.db import models

class ClearanceItem(models.Model):
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=50)  # library, hostel, finance, department
    description = models.CharField(max_length=200)
    is_required = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

class StudentClearance(models.Model):
    student = models.ForeignKey('student.StudentProfile', on_delete=models.CASCADE)
    session = models.ForeignKey('academic.AcademicSession', on_delete=models.CASCADE)
    items = models.JSONField(default=dict)  # {library: false, hostel: false, ...}
    status = models.CharField(max_length=20, default='pending')  # pending, in_progress, completed
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
