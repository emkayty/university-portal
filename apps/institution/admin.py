"""Institution Admin Configuration"""
from django.contrib import admin
from apps.institution.models import InstitutionSettings, Department, Faculty


@admin.register(InstitutionSettings)
class InstitutionSettingsAdmin(admin.ModelAdmin):
    list_display = ['institution_name', 'session']
    fieldsets = [
        ('Basic Info', {'fields': ['institution_name', 'short_name', 'logo', 'motto']}),
        ('Branding', {'fields': ['primary_color', 'secondary_color']}),
        ('Academic', {'fields': ['grading_system', 'session', 'current_semester']}),
    ]


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'dean', 'established']
    search_fields = ['name', 'code']


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'faculty', 'hod']
    list_filter = ['faculty']
    search_fields = ['name', 'code']
