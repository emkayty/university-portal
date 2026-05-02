import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom User Model with Roles"""
    
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('lecturer', 'Lecturer'),
        ('hod', 'Head of Department'),
        ('dean', 'Dean'),
        ('registrar', 'Registrar'),
        ('bursar', 'Bursar'),
        ('institution_admin', 'Institution Admin'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    settings_id = models.UUIDField(null=True, blank=True)  # Link to institution settings
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    class Meta:
        db_table = 'users'
        ordering = ['email']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['role']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        return self.email
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip() or self.email
    
    def has_role(self, *roles):
        """Check if user has any of the specified roles"""
        return self.role in roles
    
    def is_student(self):
        return self.role == 'student'
    
    def is_lecturer(self):
        return self.role == 'lecturer'
    
    def is_hod(self):
        return self.role == 'hod'
    
    def is_dean(self):
        return self.role == 'dean'
    
    def is_registrar(self):
        return self.role == 'registrar'
    
    def is_bursar(self):
        return self.role == 'bursar'
    
    def is_institution_admin(self):
        return self.role == 'institution_admin'
    
    def can_approve_results(self):
        return self.role in ['hod', 'dean', 'registrar']