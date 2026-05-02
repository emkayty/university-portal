"""Staff App - Staff Management Models"""
import uuid
from django.db import models
from django.conf import settings
from apps.academic.models import Faculty, Department


class StaffProfile(models.Model):
    """Staff Profile - extends User"""
    
    RANK_CHOICES = [
        ('professor', 'Professor'),
        ('associate_professor', 'Associate Professor'),
        ('senior_lecturer', 'Senior Lecturer'),
        ('lecturer_i', 'Lecturer I'),
        ('lecturer_ii', 'Lecturer II'),
        ('assistant_lecturer', 'Assistant Lecturer'),
        ('graduate_assistant', 'Graduate Assistant'),
    ]
    
    CONTRACT_CHOICES = [
        ('permanent', 'Permanent'),
        ('contract', 'Contract'),
        ('adjunct', 'Adjunct'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='staff_profile'
    )
    staff_id = models.CharField(max_length=20, unique=True)
    
    # Personal Info
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    
    # Employment
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='staff'
    )
    faculty = models.ForeignKey(
        Faculty,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='staff'
    )
    employment_date = models.DateField()
    rank = models.CharField(max_length=30, choices=RANK_CHOICES)
    contract_type = models.CharField(max_length=20, choices=CONTRACT_CHOICES, default='permanent')
    scheme_of_service = models.CharField(max_length=50, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'staff_profiles'
        ordering = ['staff_id']
    
    def __str__(self):
        return f"{self.staff_id} - {self.first_name} {self.last_name}"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def is_lecturer(self):
        return self.user.role == 'lecturer'


class LeaveRequest(models.Model):
    """Staff Leave Request"""
    
    LEAVE_TYPE_CHOICES = [
        ('annual', 'Annual Leave'),
        ('sick', 'Sick Leave'),
        ('maternity', 'Maternity Leave'),
        ('paternity', 'Paternity Leave'),
        ('study', 'Study Leave'),
        ('unpaid', 'Unpaid Leave'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    staff = models.ForeignKey(
        StaffProfile,
        on_delete=models.CASCADE,
        related_name='leave_requests'
    )
    leave_type = models.CharField(max_length=20, choices=LEAVE_TYPE_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_leaves'
    )
    approval_comment = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'leave_requests'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.staff.staff_id} - {self.leave_type}"
    
    @property
    def duration_days(self):
        return (self.end_date - self.start_date).days + 1


class LeaveBalance(models.Model):
    """Staff Leave Balance"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    staff = models.ForeignKey(
        StaffProfile,
        on_delete=models.CASCADE,
        related_name='leave_balances'
    )
    leave_type = models.CharField(max_length=20)
    total_days = models.IntegerField(default=0)
    used_days = models.IntegerField(default=0)
    session = models.ForeignKey(
        'academic.AcademicSession',
        on_delete=models.CASCADE,
        related_name='leave_balances'
    )
    
    class Meta:
        db_table = 'leave_balances'
        unique_together = ['staff', 'leave_type', 'session']
    
    @property
    def remaining_days(self):
        return self.total_days - self.used_days


class PromotionRecord(models.Model):
    """Staff Promotion Record"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    staff = models.ForeignKey(
        StaffProfile,
        on_delete=models.CASCADE,
        related_name='promotions'
    )
    from_rank = models.CharField(max_length=30)
    to_rank = models.CharField(max_length=30)
    effective_date = models.DateField()
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_promotions'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'promotion_records'
        ordering = ['-effective_date']
    
    def __str__(self):
        return f"{self.staff.staff_id} - {self.from_rank} to {self.to_rank}"


class StaffAppraisal(models.Model):
    """Staff Appraisal"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    staff = models.ForeignKey(
        StaffProfile,
        on_delete=models.CASCADE,
        related_name='appraisals'
    )
    session = models.ForeignKey(
        'academic.AcademicSession',
        on_delete=models.CASCADE,
        related_name='staff_appraisals'
    )
    score = models.IntegerField(null=True, blank=True)
    comment = models.TextField(blank=True)
    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='staff_appraisals'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'staff_appraisals'
        ordering = ['-session', '-created_at']
    
    def __str__(self):
        return f"{self.staff.staff_id} - {self.session.name}"

# === EXTENDED STAFF FIELDS (Additional for Nigerian Standards) ===
class StaffProfileExtended(models.Model):
    """Extended staff data - Nigerian University Standards"""
    staff = models.OneToOneField(StaffProfile, on_delete=models.CASCADE)
    
    # Profile Photo
    photo = models.ImageField(upload_to='staff_photos/', null=True, blank=True)
    
    # National ID
    nin = models.CharField(max_length=11, blank=True)
    staff_type = models.CharField(max_length=20, default='academic')
    
    # Additional Contact
    alt_phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    state_of_origin = models.CharField(max_length=50, blank=True)
    
    # Emergency Contact
    emergency_contact_name = models.CharField(max_length=100, blank=True)
    emergency_contact_phone = models.CharField(max_length=20, blank=True)
    emergency_contact_relationship = models.CharField(max_length=50, blank=True)
    
    # Bank Details
    bank_name = models.CharField(max_length=50, blank=True)
    account_number = models.CharField(max_length=10, blank=True)
    account_name = models.CharField(max_length=100, blank=True)
    
    # Qualifications
    highest_qualification = models.CharField(max_length=50, blank=True)
    specialization = models.CharField(max_length=100, blank=True)
    publications = models.IntegerField(default=0)
