"""Student Admin Configuration"""
from django.contrib import admin
from apps.student.models import StudentProfile, AdmissionApplication, CourseRegistration, Result


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ['matric_number', 'full_name', 'programme', 'current_level', 'admission_status']
    list_filter = ['admission_status', 'programme', 'current_level']
    search_fields = ['matric_number', 'first_name', 'last_name']
    raw_id_fields = ['user']


@admin.register(AdmissionApplication)
class AdmissionApplicationAdmin(admin.ModelAdmin):
    list_display = ['student_profile', 'jamb_reg_no', 'application_session', 'status']
    list_filter = ['status', 'application_session']
    search_fields = ['jamb_reg_no']


@admin.register(CourseRegistration)
class CourseRegistrationAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'session', 'semester', 'status']
    list_filter = ['session', 'semester', 'status']


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ['registration', 'score', 'grade', 'status']
    list_filter = ['status', 'session']
