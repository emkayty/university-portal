"""Student App - Student Lifecycle Models"""
import uuid
from django.db import models
from django.conf import settings
from apps.academic.models import Programme, AcademicSession


class StudentProfile(models.Model):
    """Student Profile - extends User - Nigerian University Standards"""
    
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    
    BLOOD_TYPE_CHOICES = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-'),
    ]
    
    GENOTYPE_CHOICES = [
        ('AA', 'AA'), ('AS', 'AS'),
        ('SS', 'SS'), ('AC', 'AC'),
    ]
    
    MODE_OF_ENTRY_CHOICES = [
        ('UTME', 'UTME'),
        ('DE', 'Direct Entry'),
        ('TRANSFER', 'Transfer'),
        ('JUPEB', 'JUPEB'),
        ('PART_TIME', 'Part Time'),
    ]
    
    ADMISSION_STATUS_CHOICES = [
        ('applicant', 'Applicant'),
        ('admitted', 'Admitted'),
        ('deferred', 'Deferred'),
        ('suspended', 'Suspended'),
        ('withdrawn', 'Withdrawn'),
        ('graduated', 'Graduated'),
    ]
    
    CLEARANCE_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='student_profile'
    )
    matric_number = models.CharField(max_length=20, unique=True, null=True, blank=True)
    
    # === ESSENTIAL PERSONAL DATA (Nigerian + Global) ===
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    other_names = models.CharField(max_length=100, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    
    # === PROFILE PHOTO (ID Card) ===
    photo = models.ImageField(upload_to='student_photos/', null=True, blank=True)
    
    # === HEALTH DATA (Critical for hostel, NYSC) ===
    blood_type = models.CharField(max_length=3, choices=BLOOD_TYPE_CHOICES, blank=True)
    genotype = models.CharField(max_length=2, choices=GENOTYPE_CHOICES, blank=True)
    disabilities = models.TextField(blank=True)  # Accessibility needs
    
    # === NATIONAL IDENTIFICATION (NIN) ===
    nin = models.CharField(max_length=11, blank=True)  # National ID Number
    international_passport = models.CharField(max_length=20, blank=True)
    
    # === CONTACT DATA ===
    phone = models.CharField(max_length=20, blank=True)
    alt_phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    
    # === GEOGRAPHIC (Nigerian) ===
    nationality = models.CharField(max_length=50, default='Nigerian')
    state_of_origin = models.CharField(max_length=50, blank=True)
    lga = models.CharField(max_length=50, blank=True)
    state_of_residence = models.CharField(max_length=50, blank=True)
    district = models.CharField(max_length=50, blank=True)
    
    # === EMERGENCY CONTACT (Critical) ===
    emergency_contact_name = models.CharField(max_length=100, blank=True)
    emergency_contact_phone = models.CharField(max_length=20, blank=True)
    emergency_contact_relationship = models.CharField(max_length=50, blank=True)
    emergency_contact_address = models.TextField(blank=True)
    
    # === NEXT OF KIN ===
    next_of_kin_name = models.CharField(max_length=100, blank=True)
    next_of_kin_phone = models.CharField(max_length=20, blank=True)
    next_of_kin_relationship = models.CharField(max_length=50, blank=True)
    next_of_kin_address = models.TextField(blank=True)
    
    # === BANK DETAILS (For refunds, allowances) ===
    bank_name = models.CharField(max_length=50, blank=True)
    account_number = models.CharField(max_length=10, blank=True)
    account_name = models.CharField(max_length=100, blank=True)
    
    # === ACADEMIC ===
    admission_session = models.ForeignKey(
        AcademicSession,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='admitted_students'
    )
    mode_of_entry = models.CharField(max_length=20, choices=MODE_OF_ENTRY_CHOICES, default='UTME')
    admission_status = models.CharField(max_length=20, choices=ADMISSION_STATUS_CHOICES, default='applicant')
    current_level = models.IntegerField(default=100)
    programme = models.ForeignKey(
        Programme,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='students'
    )
    
    # === PREVIOUS EDUCATION ===
    previous_school_1 = models.CharField(max_length=100, blank=True)
    previous_school_1_year = models.IntegerField(null=True, blank=True)
    previous_school_2 = models.CharField(max_length=100, blank=True)
    previous_school_2_year = models.IntegerField(null=True, blank=True)
    
    # === CLEARANCE ===
    clearance_status = models.JSONField(default=dict)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'student_profiles'
        ordering = ['matric_number']
    
    def __str__(self):
        return self.matric_number or f"Student {self.id}"
    
    @property
    def full_name(self):
        names = [self.first_name]
        if self.other_names:
            names.append(self.other_names)
        names.append(self.last_name)
        return ' '.join(names)
    
    def generate_matric_number(self):
        """Generate matriculation number"""
        if not self.matric_number and self.admission_session:
            prefix = f"{self.admission_session.name[:4]}"
            # Simple counter - in production use a proper sequence
            count = StudentProfile.objects.filter(
                admission_session=self.admission_session
            ).count() + 1
            self.matric_number = f"{prefix}{self.programme.code[:2]}{count:05d}"
            self.save()
        return self.matric_number
    
    @property
    def is_active(self):
        return self.admission_status == 'admitted'
    
    @property
    def clearance_progress(self):
        """Calculate clearance progress percentage"""
        total = len(self.clearance_status) if self.clearance_status else 4
        completed = sum(1 for v in self.clearance_status.values() if v)
        return int((completed / total) * 100) if total > 0 else 0


class AdmissionApplication(models.Model):
    """Admission Application"""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('under_review', 'Under Review'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student_profile = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name='applications'
    )
    
    # JAMB Details
    jamb_reg_no = models.CharField(max_length=20, blank=True)
    jamb_score = models.IntegerField(null=True, blank=True)
    
    # O-Level Results
    o_level_result = models.JSONField(default=list)  # [{subject: '', grade: ''}]
    
    application_session = models.ForeignKey(
        AcademicSession,
        on_delete=models.CASCADE,
        related_name='applications'
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewed_applications'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'admission_applications'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Application {self.id} - {self.student_profile.full_name}"


class CourseRegistration(models.Model):
    """Student Course Registration"""
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('dropped', 'Dropped'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name='registrations'
    )
    course = models.ForeignKey(
        'academic.Course',
        on_delete=models.CASCADE,
        related_name='registrations'
    )
    session = models.ForeignKey(
        AcademicSession,
        on_delete=models.CASCADE,
        related_name='registrations'
    )
    semester = models.ForeignKey(
        'academic.Semester',
        on_delete=models.CASCADE,
        related_name='registrations'
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    registered_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'course_registrations'
        unique_together = ['student', 'course', 'session', 'semester']
        ordering = ['-registered_at']
    
    def __str__(self):
        return f"{self.student.matric_number} - {self.course.code}"


class TimetableEntry(models.Model):
    """Timetable Entry"""
    
    DAY_CHOICES = [
        (1, 'Monday'),
        (2, 'Tuesday'),
        (3, 'Wednesday'),
        (4, 'Thursday'),
        (5, 'Friday'),
        (6, 'Saturday'),
        (7, 'Sunday'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course = models.ForeignKey(
        'academic.Course',
        on_delete=models.CASCADE,
        related_name='timetable_entries'
    )
    day_of_week = models.IntegerField(choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    venue = models.CharField(max_length=100)
    session = models.ForeignKey(
        AcademicSession,
        on_delete=models.CASCADE,
        related_name='timetable_entries'
    )
    
    class Meta:
        db_table = 'timetable_entries'
        unique_together = ['course', 'day_of_week', 'start_time', 'session']
        ordering = ['day_of_week', 'start_time']
    
    def __str__(self):
        return f"{self.course.code} - {self.get_day_of_week_display()} {self.start_time}"


class Result(models.Model):
    """Student Result"""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    registration = models.ForeignKey(
        CourseRegistration,
        on_delete=models.CASCADE,
        related_name='results'
    )
    session = models.ForeignKey(
        AcademicSession,
        on_delete=models.CASCADE,
        related_name='results'
    )
    semester = models.ForeignKey(
        'academic.Semester',
        on_delete=models.CASCADE,
        related_name='results'
    )
    lecturer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='submitted_results'
    )
    score = models.DecimalField(max_digits=5, decimal_places=2)
    grade = models.CharField(max_length=2)
    grade_point = models.DecimalField(max_digits=3, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    
    # Approval workflow
    approved_by_hod = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='hod_approved_results'
    )
    hod_comment = models.TextField(blank=True)
    approved_by_dean = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='dean_approved_results'
    )
    dean_comment = models.TextField(blank=True)
    approved_by_senate = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='senate_approved_results'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'results'
        ordering = ['-session', '-semester', 'registration__course']
    
    def __str__(self):
        return f"{self.registration.student.matric_number} - {self.registration.course.code}"


class CGPAHistory(models.Model):
    """CGPA History"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name='cgpa_history'
    )
    session = models.ForeignKey(
        AcademicSession,
        on_delete=models.CASCADE,
        related_name='cgpa_history'
    )
    semester = models.ForeignKey(
        'academic.Semester',
        on_delete=models.CASCADE,
        related_name='cgpa_history'
    )
    gpa = models.DecimalField(max_digits=3, decimal_places=2)
    cumulative_gpa = models.DecimalField(max_digits=3, decimal_places=2)
    
    class Meta:
        db_table = 'cgpa_history'
        unique_together = ['student', 'session', 'semester']
    
    def __str__(self):
        return f"{self.student.matric_number} - {self.cumulative_gpa}"


class GraduationClearance(models.Model):
    """Graduation Clearance"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.OneToOneField(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name='graduation_clearance'
    )
    cleared_by_library = models.BooleanField(default=False)
    cleared_by_hostel = models.BooleanField(default=False)
    cleared_by_bursary = models.BooleanField(default=False)
    cleared_by_department = models.BooleanField(default=False)
    cleared_at = models.DateTimeField(null=True, blank=True)
    eligible_to_graduate = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'graduation_clearance'
    
    def __str__(self):
        return f"Clearance - {self.student.matric_number}"
    
    @property
    def progress(self):
        total = 4
        completed = sum([
            self.cleared_by_library,
            self.cleared_by_hostel,
            self.cleared_by_bursary,
            self.cleared_by_department
        ])
        return int((completed / total) * 100)


class Transcript(models.Model):
    """Official Transcript"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name='transcripts'
    )
    issued_at = models.DateTimeField(auto_now_add=True)
    pdf_url = models.URLField(blank=True)
    qr_verification_code = models.CharField(max_length=50, unique=True)
    
    class Meta:
        db_table = 'transcripts'
        ordering = ['-issued_at']
    
    def __str__(self):
        return f"Transcript - {self.student.matric_number}"