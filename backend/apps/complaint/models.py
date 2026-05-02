"""Complaint Management Models"""
from django.db import models

class Complaint(models.Model):
    student = models.ForeignKey('student.StudentProfile', on_delete=models.CASCADE)
    category = models.CharField(max_length=50)  # academic, hostel, finance, others
    subject = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, default='pending')  # pending, assigned, resolved, rejected
    assigned_to = models.ForeignKey('staff.StaffProfile', on_delete=models.SET_NULL, null=True, related_name='assigned_complaints')
    response = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
