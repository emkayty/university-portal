"""
Database Index Optimizations
=====================
Adds critical indexes for query performance improvements.
Run: python manage.py migrate
"""
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0001_initial'),
        ('academic', '0001_initial'),
        ('learning', '0001_initial'),
        ('finance', '0001_initial'),
    ]

    operations = [
        # Student Indexes
        migrations.AddIndex(
            model_name='studentprofile',
            index=models.Index(fields=['matric_number'], name='idx_matric_number_unique'),
        ),
        migrations.AddIndex(
            model_name='studentprofile',
            index=models.Index(fields=['user'], name='idx_user_profile'),
        ),
        
        # Academic Indexes
        migrations.AddIndex(
            model_name='academicsession',
            index=models.Index(fields=['is_current'], name='idx_is_current_session'),
        ),
        migrations.AddIndex(
            model_name='semester',
            index=models.Index(fields=['session', 'name'], name='idx_semester_session'),
        ),
        
        # Learning Indexes  
        migrations.AddIndex(
            model_name='attendancerecord',
            index=models.Index(fields=['session', 'student'], name='idx_attendance_session'),
        ),
        migrations.AddIndex(
            model_name='attendancerecord',
            index=models.Index(fields=['timestamp'], name='idx_attendance_time'),
        ),
        
        # Finance Indexes
        migrations.AddIndex(
            model_name='payment',
            index=models.Index(fields=['student', 'status'], name='idx_payment_status'),
        ),
        migrations.AddIndex(
            model_name='payment',
            index=models.Index(fields=['paid_at'], name='idx_payment_date'),
        ),
        
        # Results Index
        migrations.AddIndex(
            model_name='result',
            index=models.Index(fields=['registration', 'status'], name='idx_result_status'),
        ),
    ]