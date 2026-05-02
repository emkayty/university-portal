"""Additional Academic Models - Course Allocation, Hostel"""
import uuid
from django.db import models
from django.conf import settings


class Hostel(models.Model):
    """Hostel/Accommodation Building"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=10, unique=True)
    gender = models.CharField(max_length=10, choices=[
        ('male', 'Male'),
        ('female', 'Female'),
        ('mixed', 'Mixed'),
    ], default='mixed')
    total_beds = models.IntegerField(default=0)
    available_beds = models.IntegerField(default=0)
    warden = models.ForeignKey(
        'StaffProfile', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='hostels_warden'
    )
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'hostels'
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.gender})"


class Room(models.Model):
    """Hostel Room"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE, related_name='rooms')
    room_number = models.CharField(max_length=20)
    floor = models.IntegerField(default=1)
    capacity = models.IntegerField(default=4)  # beds in room
    current_occupants = models.IntegerField(default=0)
    room_type = models.CharField(max_length=20, choices=[
        ('single', 'Single'),
        ('double', 'Double'),
        ('triple', 'Triple'),
        ('4-in-1', '4-in-1'),
    ], default='4-in-1')
    gender = models.CharField(max_length=10)
    fee = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    is_available = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'rooms'
        unique_together = ['hostel', 'room_number']
    
    def __str__(self):
        return f"{self.hostel.name} - Room {self.room_number}"


class HostelAllocation(models.Model):
    """Student Hostel Allocation"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey('StudentProfile', on_delete=models.CASCADE, related_name='hostel_allocations')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='allocations')
    session = models.ForeignKey('AcademicSession', on_delete=models.CASCADE)
    bed_number = models.CharField(max_length=10)
    check_in_date = models.DateField(null=True, blank=True)
    check_out_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    allocated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True
    )
    allocated_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'hostel_allocations'
        unique_together = ['student', 'session', 'is_active']


class CourseAllocation(models.Model):
    """Course Lecturer Allocation per Semester"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='allocations')
    lecturer = models.ForeignKey('StaffProfile', on_delete=models.CASCADE, related_name='course_allocations')
    session = models.ForeignKey('AcademicSession', on_delete=models.CASCADE)
    semester = models.ForeignKey('Semester', on_delete=models.CASCADE)
    is_primary = models.BooleanField(default=True)  # primary lecturer
    workload_hours = models.IntegerField(default=3)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'course_allocations'
        unique_together = ['course', 'session', 'semester', 'lecturer']


class CarryOverCourse(models.Model):
    """Carry-over Course Tracking"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey('StudentProfile', on_delete=models.CASCADE, related_name='carryover_courses')
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    original_session = models.ForeignKey('AcademicSession', on_delete=models.CASCADE, related_name='original_carryovers')
    original_semester = models.ForeignKey('Semester', on_delete=models.CASCADE)
    attempt_count = models.IntegerField(default=1)
    is_cleared = models.BooleanField(default=False)
    cleared_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'carryover_courses'
        unique_together = ['student', 'course', 'original_session']


class AcademicWarning(models.Model):
    """Academic Warning/Probation Tracking"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey('StudentProfile', on_delete=models.CASCADE, related_name='academic_warnings')
    session = models.ForeignKey('AcademicSession', on_delete=models.CASCADE)
    semester = models.ForeignKey('Semester', on_delete=models.CASCADE)
    warning_type = models.CharField(max_length=50, choices=[
        ('probation', 'Academic Probation'),
        ('suspension', 'Suspension'),
        ('withdrawal', 'Required Withdrawal'),
    ])
    gpa_before = models.DecimalField(max_digits=4, decimal_places=2)
    reason = models.TextField()
    is_active = models.BooleanField(default=True)
    cleared_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'academic_warnings'
        ordering = ['-created_at']