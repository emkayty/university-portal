"""Institution Admin Configuration"""
from django.contrib import admin
from .models import InstitutionSettings


@admin.register(InstitutionSettings)
class InstitutionSettingsAdmin(admin.ModelAdmin):
    list_display = ['institution_name', 'created_at', 'updated_at']
    readonly_fields = ['id', 'created_at', 'updated_at']
    fieldsets = (
        ('Basic Info', {
            'fields': ('institution_name', 'motto', 'primary_color', 'secondary_color')
        }),
        ('Grading', {
            'fields': ('grading_scale_type', 'grading_boundaries', 'pass_mark', 'max_score')
        }),
        ('Academic Calendar', {
            'fields': ('academic_year_start', 'semester_structure')
        }),
        ('Payment', {
            'fields': ('payment_gateway',)
        }),
    )