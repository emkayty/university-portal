"""Staff Admin Configuration"""
from django.contrib import admin
from apps.staff.models import StaffProfile, Lecturer


@admin.register(StaffProfile)
class StaffProfileAdmin(admin.ModelAdmin):
    list_display = ['employee_id', 'full_name', 'department', 'position']
    list_filter = ['department', 'position']
    search_fields = ['employee_id', 'first_name', 'last_name']


@admin.register(Lecturer)
class LecturerAdmin(admin.ModelAdmin):
    list_display = ['staff', 'department', 'staff_code']
    list_filter = ['department']
