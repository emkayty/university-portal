"""Complete User Profile Models - Extended with Nigerian & International Data"""
import uuid
from django.db import models
from django.conf import settings
from apps.academic.models import Programme, AcademicSession


class ExtendedUserProfile(models.Model):
    """Extended User Profile with Comprehensive Data"""
    
    # Basic Info (supplements User model)
    title = models.CharField(max_length=10, blank=True)  # Mr, Mrs, Miss, etc.
    other_names = models.CharField(max_length=100, blank=True)
    maiden_name = models.CharField(max_length=100, blank=True)  # For married women
    
    # Personal Details
    date_of_birth = models.DateField(null=True, blank=True)
    place_of_birth = models.CharField(max_length=200, blank=True)
    gender = models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female')])
    marital_status = models.CharField(max_length=20, blank=True)
    
    # Nationality & Origin
    nationality = models.CharField(max_length=3, default='NG')  # ISO country code
    state_of_origin = models.CharField(max_length=50, blank=True)  # Nigerian state
    local_government_area = models.CharField(max_length=100, blank=True)
    hometown = models.CharField(max_length=200, blank=True)
    
    # Contact Details
    phone_number_1 = models.CharField(max_length=20, blank=True)
    phone_number_2 = models.CharField(max_length=20, blank=True)
    email_address = models.EmailField(blank=True)
    residential_address = models.TextField(blank=True)
    permanent_address = models.TextField(blank=True)
    
    # Religion
    religion = models.CharField(max_length=30, blank=True)
    denomination = models.CharField(max_length=50, blank=True)
    
    # Medical Information
    blood_group = models.CharField(max_length=5, blank=True)  # A+, B+, etc.
    genotype = models.CharField(max_length=10, blank=True)  # AA, AS, SS
    medical_conditions = models.JSONField(default=list)  # List of conditions
    disabilities = models.JSONField(default=list)  # List of disabilities
    allergies = models.TextField(blank=True)
    current_medications = models.TextField(blank=True)
    
    # Emergency Contact
    emergency_contact_name = models.CharField(max_length=200, blank=True)
    emergency_contact_phone = models.CharField(max_length=20, blank=True)
    emergency_contact_relationship = models.CharField(max_length=30, blank=True)
    emergency_contact_address = models.TextField(blank=True)
    
    # Profile Photo
    passport_photograph = models.URLField(blank=True)
    signature = models.URLField(blank=True)
    
    # Biometric Data
    fingerprint_template = models.BinaryField(null=True, blank=True)
    facial_template = models.BinaryField(null=True, blank=True)
    
    # Verification
    is_bio_verified = models.BooleanField(default=False)
    is_document_verified = models.BooleanField(default=False)
    verification_level = models.CharField(max_length=20, default='none')  # none, basic, full
    
    # Social Media
    linkedin_url = models.URLField(blank=True)
    twitter_handle = models.CharField(max_length=50, blank=True)
    facebook_url = models.URLField(blank=True)
    instagram_handle = models.CharField(max_length=50, blank=True)
    
    # Reference Details
    referee_1_name = models.CharField(max_length=200, blank=True)
    referee_1_phone = models.CharField(max_length=20, blank=True)
    referee_1_email = models.EmailField(blank=True)
    referee_1_address = models.TextField(blank=True)
    
    referee_2_name = models.CharField(max_length=200, blank=True)
    referee_2_phone = models.CharField(max_length=20, blank=True)
    referee_2_email = models.EmailField(blank=True)
    referee_2_address = models.TextField(blank=True)
    
    # Social History
    convicted = models.BooleanField(default=False)
    conviction_details = models.TextField(blank=True)
    currently_employed = models.BooleanField(default=True)
    employer_name = models.CharField(max_length=200, blank=True)
    employer_address = models.TextField(blank=True)
    job_title = models.CharField(max_length=100, blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'extended_user_profiles'
    
    def __str__(self):
        return f"Extended Profile - {self.user.email if hasattr(self, 'user') else self.id}"


class StudentExtendedProfile(ExtendedUserProfile):
    """Student-Specific Extended Profile"""
    
    # Student-Specific Fields
    student = models.OneToOneField(
        'student.StudentProfile',
        on_delete=models.CASCADE,
        related_name='extended_profile'
    )
    
    # JAMB Details
    jamb_reg_no = models.CharField(max_length=20, blank=True)
    jamb_score = models.IntegerField(null=True, blank=True)
    jamb_year = models.IntegerField(null=True, blank=True)
    
    # O-Level Results (multiple sittings)
    o_level_sitting_1 = models.JSONField(default=dict)  # {subject: grade}
    o_level_sitting_2 = models.JSONField(default=dict)
    o_level_exam_type = models.CharField(max_length=20, blank=True)  # WAEC, NECO
    
    # Tertiary Qualifications
    previous_degrees = models.JSONField(default=list)  # [{institution, degree, year}]
    professional_qualifications = models.JSONField(default=list)
    
    # Admission Details
    mode_of_entry = models.CharField(max_length=30, blank=True)
    admission_year = models.IntegerField(null=True, blank=True)
    graduation_year = models.IntegerField(null=True, blank=True)
    
    # Health Insurance
    nhf_number = models.CharField(max_length=20, blank=True)
    nhis_number = models.CharField(max_length=20, blank=True)
    health_insurance_provider = models.CharField(max_length=100, blank=True)
    
    # Sponsor Details
    sponsor_name = models.CharField(max_length=200, blank=True)
    sponsor_relationship = models.CharField(max_length=30, blank=True)
    sponsor_phone = models.CharField(max_length=20, blank=True)
    sponsor_address = models.TextField(blank=True)
    sponsor_annual_income = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    
    # Guardian (for minors)
    guardian_name = models.CharField(max_length=200, blank=True)
    guardian_relationship = models.CharField(max_length=30, blank=True)
    guardian_phone = models.CharField(max_length=20, blank=True)
    guardian_email = models.EmailField(blank=True)
    guardian_address = models.TextField(blank=True)
    
    class Meta:
        db_table = 'student_extended_profiles'
    
    def __str__(self):
        return f"Student Extended - {self.student.matric_number}"


class StaffExtendedProfile(ExtendedUserProfile):
    """Staff-Specific Extended Profile"""
    
    # Staff-Specific Fields
    staff = models.OneToOneField(
        'staff.StaffProfile',
        on_delete=models.CASCADE,
        related_name='extended_profile'
    )
    
    # Professional Details
    professional_qualifications = models.JSONField(default=list)
    publications = models.JSONField(default=list)
    research_interests = models.JSONField(default=list)
    conferences_attended = models.JSONField(default=list)
    
    # Employment History
    previous_employment = models.JSONField(default=list)  # [{institution, position, from_date, to_date}]
    
    # Bank Details (for payroll)
    bank_name = models.CharField(max_length=100, blank=True)
    account_number = models.CharField(max_length=20, blank=True)
    account_name = models.CharField(max_length=200, blank=True)
    
    # Pension
    pension_provider = models.CharField(max_length=100, blank=True)
    pension_pin = models.CharField(max_length=30, blank=True)
    
    # Professional Associations
    professional_bodies = models.JSONField(default=list)  # [{body, membership_no, year}]
    licenses = models.JSONField(default=list)  # [{license, number, expiry}]
    
    # International Details
    passport_number = models.CharField(max_length=30, blank=True)
    passport_expiry = models.DateField(null=True, blank=True)
    passport_country = models.CharField(max_length=3, blank=True)
    
    # ID Numbers
    tin_number = models.CharField(max_length=20, blank=True)
    driver_license = models.CharField(max_length=30, blank=True)
    
    class Meta:
        db_table = 'staff_extended_profiles'
    
    def __str__(self):
        return f"Staff Extended - {self.staff.staff_id}"


class NextOfKin(models.Model):
    """Next of Kin Information"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='next_of_kin'
    )
    
    full_name = models.CharField(max_length=200)
    relationship = models.CharField(max_length=30)
    
    # Contact Details
    phone_number = models.CharField(max_length=20, blank=True)
    alternative_phone = models.CharField(max_length=20, blank=True)
    email_address = models.EmailField(blank=True)
    address = models.TextField()
    
    # Additional Details
    occupation = models.CharField(max_length=100, blank=True)
    employer = models.CharField(max_length=200, blank=True)
    
    is_primary = models.BooleanField(default=True)
    is_emergency_contact = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'next_of_kin'
        ordering = ['-is_primary', '-created_at']
    
    def __str__(self):
        return f"{self.full_name} ({self.relationship}) - {self.user.email}"


class ContactAddress(models.Model):
    """Multiple Contact Addresses"""
    
    ADDRESS_TYPE_CHOICES = [
        ('residential', 'Residential'),
        ('permanent', 'Permanent'),
        ('office', 'Office'),
        ('billing', 'Billing'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='addresses'
    )
    
    address_type = models.CharField(max_length=20, choices=ADDRESS_TYPE_CHOICES, default='residential')
    
    # Address Lines
    street_address = models.TextField()
    street_address_line_2 = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    lga = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=3, default='NG')
    
    # Geolocation
    latitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    
    is_default = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'contact_addresses'
        ordering = ['-is_default', '-created_at']
    
    def __str__(self):
        return f"{self.address_type}: {self.street_address}, {self.city}"


class PhoneNumber(models.Model):
    """Multiple Phone Numbers"""
    
    PHONE_TYPE_CHOICES = [
        ('mobile', 'Mobile'),
        ('home', 'Home'),
        ('office', 'Office'),
        ('fax', 'Fax'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='phone_numbers'
    )
    
    phone_type = models.CharField(max_length=20, choices=PHONE_TYPE_CHOICES, default='mobile')
    phone_number = models.CharField(max_length=20)
    country_code = models.CharField(max_length=5, default='+234')
    is_verified = models.BooleanField(default=False)
    is_default = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'phone_numbers'
        ordering = ['-is_default', '-created_at']
    
    def __str__(self):
        return f"{self.country_code}{self.phone_number} ({self.phone_type})"


class UserDocument(models.Model):
    """User Documents (ID, Certificates, etc.)"""
    
    DOCUMENT_TYPE_CHOICES = [
        ('id_card', 'National ID'),
        ('passport', 'International Passport'),
        ('drivers_license', "Driver's License"),
        ('voters_card', "Voter's Card"),
        ('birth_certificate', 'Birth Certificate'),
        ('ssce_certificate', 'SSCE Certificate'),
        ('degree_certificate', 'Degree Certificate'),
        ('medical_report', 'Medical Report'),
        ('disability_certificate', 'Disability Certificate'),
        ('other', 'Other'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='documents'
    )
    
    document_type = models.CharField(max_length=30, choices=DOCUMENT_TYPE_CHOICES)
    document_number = models.CharField(max_length=50, blank=True)
    document_url = models.URLField(blank=True)
    
    # For expiry tracking
    issue_date = models.DateField(null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    
    is_verified = models.BooleanField(default=False)
    verified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='verified_documents'
    )
    verified_at = models.DateTimeField(null=True, blank=True)
    
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'user_documents'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.document_type} - {self.user.email}"