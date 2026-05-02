"""Academic Admin Configuration"""
from django.contrib import admin
from .models import Faculty, Department, Programme, Course, AcademicSession, Semester, GradingPolicy


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'dean']
    search_fields = ['name', 'code']


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'faculty']
    list_filter = ['faculty']
    search_fields = ['name', 'code']


@admin.register(Programme)
class ProgrammeAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'department', 'duration_years']
    list_filter = ['department', 'duration_years']
    search_fields = ['name', 'code']


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['code', 'title', 'programme', 'level', 'credit_units']
    list_filter = ['level', 'semester_offered']
    search_fields = ['code', 'title']


@admin.register(AcademicSession)
class AcademicSessionAdmin(admin.ModelAdmin):
    list_display = ['name', 'start_date', 'end_date', 'is_current']
    list_filter = ['is_current']


@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ['name', 'session', 'start_date', 'end_date']


@admin.register(GradingPolicy)
class GradingPolicyAdmin(admin.ModelAdmin):
    list_display = ['name', 'scale_type', 'pass_mark']
    list_filter = ['scale_type']