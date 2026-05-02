"""Additional Student Models - NYSC, ID Card, Alumni"""
import uuid
from django.db import models


class NYSCData(models.Model):
    """NYSC mobilization data for graduates"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.OneToOneField('StudentProfile', on_delete=models.CASCADE, related_name='nysc_data')
    
    # NYSC required fields
    state_code = models.CharField(max_length=10)  # e.g., "OG/24A"
    callup_number = models.CharField(max_length=50, unique=True)
    nysc_year = models.IntegerField()
    
    # PPA details
    ppa_state = models.CharField(max_length=100)
    ppa_lga = models.CharField(max_length=100)
    ppa_organisation = models.CharField(max_length=255)
    
    # Service status
    service_status = models.CharField(max_length=50, choices=[
        ('pending', 'Pending'),
        ('posted', 'Posted'),
        ('service_ongoing', 'Service Ongoing'),
        ('completed', 'Service Completed'),
        ('exempted', 'Exempted'),
    ], default='pending')
    
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    certificate_number = models.CharField(max_length=50, blank=True)
    
    # Bio data for NYSC
    date_of_birth = models.DateField()
    place_of_birth = models.CharField(max_length=100)
    guardian_name = models.CharField(max_length=255)
    guardian_address = models.TextField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'nysc_data'
        verbose_name = 'NYSC Data'
        verbose_name_plural = 'NYSC Data'
    
    def __str__(self):
        return f"{self.student} - {self.callup_number}"


class StudentIDCard(models.Model):
    """Student ID Card Management"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.OneToOneField('StudentProfile', on_delete=models.CASCADE, related_name='id_card')
    
    card_number = models.CharField(max_length=50, unique=True)
    card_type = models.CharField(max_length=20, choices=[
        ('temporary', 'Temporary'),
        ('permanent', 'Permanent'),
        ('visitor', 'Visitor'),
    ], default='temporary')
    
    # Photo
    photo_url = models.URLField(blank=True)
    photo_captured_at = models.DateTimeField(null=True, blank=True)
    
    # Status
    is_approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey(
        'StaffProfile',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='id_cards_approved'
    )
    approved_at = models.DateTimeField(null=True, blank=True)
    
    issue_date = models.DateField(null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    barcode = models.CharField(max_length=100, blank=True)
    qr_code = models.CharField(max_length=100, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'student_id_cards'
    
    def __str__(self):
        return f"{self.student} - {self.card_number}"


class Alumni(models.Model):
    """Alumni Tracking"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.OneToOneField('StudentProfile', on_delete=models.CASCADE, related_name='alumni')
    
    # Graduation details
    graduation_year = models.IntegerField()
    convocation_batch = models.CharField(max_length=20, blank=True)
    class_of_degree = models.CharField(max_length=20, choices=[
        ('first_class', 'First Class'),
        ('second_class_upper', 'Second Class (Upper)'),
        ('second_class_lower', 'Second Class (Lower)'),
        ('third_class', 'Third Class'),
        ('pass', 'Pass'),
    ])
    
    # Current employment
    current_employer = models.CharField(max_length=255, blank=True)
    job_title = models.CharField(max_length=100, blank=True)
    employment_sector = models.CharField(max_length=50, choices=[
        ('public', 'Public Sector'),
        ('private', 'Private Sector'),
        ('self_employed', 'Self Employed'),
        ('ngos', 'NGO/INGO'),
        ('entrepreneur', 'Entrepreneur'),
        ('further_study', 'Further Study'),
        ('unemployed', 'Unemployed'),
    ], default='unemployed')
    
    # Contact
    mobile_phone = models.CharField(max_length=20, blank=True)
    linkedin_url = models.URLField(blank=True)
    twitter_handle = models.CharField(max_length=50, blank=True)
    
    is_verified = models.BooleanField(default=False)
    verified_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'alumni'
        verbose_name = 'Alumni'
        verbose_name_plural = 'Alumni'
    
    def __str__(self):
        return f"{self.student} - Class of {self.graduation_year}"


class MedicalRecord(models.Model):
    """Student Medical Records"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey('StudentProfile', on_delete=models.CASCADE, related_name='medical_records')
    
    blood_group = models.CharField(max_length=5)
    genotype = models.CharField(max_length=5)
    
    # Medical conditions
    has_allergies = models.BooleanField(default=False)
    allergies_detail = models.TextField(blank=True)
    has_chronic_conditions = models.BooleanField(default=False)
    conditions_detail = models.TextField(blank=True)
    on_medication = models.BooleanField(default=False)
    medication_detail = models.TextField(blank=True)
    
    # Disability/Accessibility
    has_disability = models.BooleanField(default=False)
    disability_type = models.CharField(max_length=100, blank=True)
    disability_detail = models.TextField(blank=True)
    requires_special_accommodation = models.BooleanField(default=False)
    
    # Emergency contact
    emergency_contact_name = models.CharField(max_length=255)
    emergency_contact_phone = models.CharField(max_length=20)
    emergency_contact_relationship = models.CharField(max_length=50)
    
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'medical_records'
    
    def __str__(self):
        return f"{self.student} - Medical Record"