"""Institution App - Settings & Setup"""
import uuid
from django.db import models
from django.conf import settings


class InstitutionSettings(models.Model):
    """Institution Configuration - Singleton per instance"""
    
    GRADING_SCALE_CHOICES = [
        ('british', 'British/Nigerian (A=70+, 5.0 scale)'),
        ('american', 'American (A=90+, 4.0 scale)'),
        ('custom', 'Custom'),
    ]
    
    GATEWAY_CHOICES = [
        ('paystack', 'Paystack'),
        ('flutterwave', 'Flutterwave'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    institution_name = models.CharField(max_length=255)
    motto = models.CharField(max_length=500, blank=True)
    logo_url = models.URLField(blank=True)
    primary_color = models.CharField(max_length=7, default='#1e40af')  # Blue
    secondary_color = models.CharField(max_length=7, default='#059669')  # Green
    
    # Grading
    grading_scale_type = models.CharField(max_length=20, choices=GRADING_SCALE_CHOICES, default='british')
    grading_boundaries = models.JSONField(default=dict)  # {'A': 70, 'B': 60, ...}
    pass_mark = models.IntegerField(default=40)
    max_score = models.IntegerField(default=100)
    cgpa_formula = models.CharField(max_length=50, default='standard')
    
    # Academic Calendar
    academic_year_start = models.DateField()
    semester_structure = models.JSONField(default=list)  # [{start, end}, ...]
    
    # Payment
    payment_gateway = models.CharField(max_length=20, choices=GATEWAY_CHOICES, default='paystack')
    paystack_secret_key = models.CharField(max_length=255, blank=True)
    flutterwave_secret_key = models.CharField(max_length=255, blank=True)
    
    # Communication
    email_provider = models.CharField(max_length=50, blank=True)
    sms_provider = models.CharField(max_length=50, blank=True)
    
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='created_institutions'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'settings'
        verbose_name_plural = 'Institution Settings'
    
    def __str__(self):
        return self.institution_name
    
    def get_grading_boundaries(self):
        """Get default grading boundaries based on scale type"""
        if self.grading_boundaries:
            return self.grading_boundaries
        
        if self.grading_scale_type == 'british':
            return {'A': 70, 'B': 60, 'C': 50, 'D': 45, 'E': 40, 'F': 0}
        elif self.grading_scale_type == 'american':
            return {'A': 90, 'B': 80, 'C': 70, 'D': 60, 'F': 0}
        else:
            return {'A': 70, 'B': 60, 'C': 50, 'D': 45, 'E': 40, 'F': 0}
    
    def get_max_grade_point(self):
        """Get max grade point based on scale"""
        if self.grading_scale_type == 'british':
            return 5.0
        elif self.grading_scale_type == 'american':
            return 4.0
        return 5.0