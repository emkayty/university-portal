"""Hostel Models - Nigerian University Standards"""
from django.db import models
from django.conf import settings

class Hostel(models.Model):
    """Hostel building"""
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female')])
    total_beds = models.IntegerField(default=0)
    available_beds = models.IntegerField(default=0)
    floor_count = models.IntegerField(default=3)
    warden = models.ForeignKey('staff.StaffProfile', on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.name} ({self.gender})"

class HostelRoom(models.Model):
    """Hostel room"""
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE)
    room_number = models.CharField(max_length=20)
    floor = models.IntegerField()
    bed_count = models.IntegerField(default=4)
    current_occupants = models.IntegerField(default=0)
    price_per_bed = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ['hostel', 'room_number']
    
    def __str__(self):
        return f"{self.hostel.name} - Room {self.room_number}"

class HostelAllocation(models.Model):
    """Student hostel allocation"""
    student = models.ForeignKey('student.StudentProfile', on_delete=models.CASCADE)
    room = models.ForeignKey(HostelRoom, on_delete=models.CASCADE)
    session = models.ForeignKey('academic.AcademicSession', on_delete=models.CASCADE)
    bed_number = models.IntegerField()
    check_in_date = models.DateField(null=True, blank=True)
    check_out_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, default='pending')  # pending, allocated, checked_in, checked_out
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.room}"
