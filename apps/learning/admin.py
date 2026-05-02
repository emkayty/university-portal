"""Learning Admin Configuration"""
from django.contrib import admin
from apps.learning.models import Course, Material, Assignment, Quiz


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['code', 'title', 'programme', 'level', 'semester']
    list_filter = ['programme', 'level', 'semester']
    search_fields = ['code', 'title']


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'material_type', 'created_at']
    list_filter = ['course', 'material_type']


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'due_date', 'total_marks']
    list_filter = ['course']


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'duration', 'total_marks']
    list_filter = ['course']
