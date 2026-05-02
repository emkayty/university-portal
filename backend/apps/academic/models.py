"""Academic App - Academic Structure Models"""
import uuid
from django.db import models
from django.conf import settings


class Faculty(models.Model):
    """Faculty/College"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=10, unique=True)
    dean = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='dean_of_faculty'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'faculties'
        ordering = ['name']
    
    def __str__(self):
        return f"{self.code} - {self.name}"


class Department(models.Model):
    """Department"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=10)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='departments')
    hod = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='hod_of_department'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'departments'
        unique_together = ['faculty', 'code']
        ordering = ['faculty', 'name']
    
    def __str__(self):
        return f"{self.code} - {self.name}"


class Programme(models.Model):
    """Programme/Course of Study"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=10)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='programmes')
    duration_years = models.IntegerField(default=4)
    grading_policy = models.ForeignKey(
        'self.GradingPolicy',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='programmes'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'programmes'
        unique_together = ['department', 'code']
        ordering = ['department', 'name']
    
    def __str__(self):
        return f"{self.code} - {self.name}"


class Course(models.Model):
    """Course/Unit"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=10)
    title = models.CharField(max_length=255)
    credit_units = models.IntegerField(default=3)
    level = models.IntegerField(default=100)  # 100, 200, 300, 400, 500
    semester_offered = models.IntegerField(choices=[
        (1, 'First Semester'),
        (2, 'Second Semester'),
        (3, 'Both'),
    ], default=3)
    programme = models.ForeignKey(Programme, on_delete=models.CASCADE, related_name='courses')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='courses')
    grading_policy = models.ForeignKey(
        'self.GradingPolicy',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='courses'
    )
    has_prerequisites = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'courses'
        unique_together = ['programme', 'code', 'level']
        ordering = ['level', 'code']
    
    def __str__(self):
        return f"{self.code} - {self.title}"


class CoursePrerequisite(models.Model):
    """Course Prerequisites"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='prerequisites')
    prerequisite = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='required_for')
    minimum_grade = models.CharField(max_length=2, blank=True)
    
    class Meta:
        db_table = 'course_prerequisites'
        unique_together = ['course', 'prerequisite']


class AcademicSession(models.Model):
    """Academic Session"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=20)  # e.g., "2024/2025"
    start_date = models.DateField()
    end_date = models.DateField()
    is_current = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'academic_sessions'
        ordering = ['-is_current', '-start_date']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if self.is_current:
            AcademicSession.objects.filter(is_current=True).exclude(pk=self.pk).update(is_current=False)
        super().save(*args, **kwargs)


class Semester(models.Model):
    """Semester within Academic Session"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session = models.ForeignKey(AcademicSession, on_delete=models.CASCADE, related_name='semesters')
    name = models.CharField(max_length=50)  # First Semester, Second Semester
    start_date = models.DateField()
    end_date = models.DateField()
    registration_start = models.DateField()
    registration_end = models.DateField()
    add_drop_end = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'semesters'
        unique_together = ['session', 'name']
        ordering = ['session', 'start_date']
    
    def __str__(self):
        return f"{self.session.name} - {self.name}"
    
    @property
    def is_registration_open(self):
        from django.utils import timezone
        now = timezone.now().date()
        return self.registration_start <= now <= self.registration_end
    
    @property
    def is_add_drop_open(self):
        from django.utils import timezone
        now = timezone.now().date()
        if self.add_drop_end:
            return self.registration_start <= now <= self.add_drop_end
        return self.is_registration_open


class GradingPolicy(models.Model):
    """Grading Policy with inheritance support"""
    
    SCALE_CHOICES = [
        ('british', 'British/Nigerian'),
        ('american', 'American'),
        ('custom', 'Custom'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    scale_type = models.CharField(max_length=20, choices=SCALE_CHOICES, default='british')
    grade_boundaries = models.JSONField(default=dict)  # {'A': 70, 'B': 60, ...}
    pass_mark = models.IntegerField(default=40)
    max_score = models.IntegerField(default=100)
    cgpa_formula = models.CharField(max_length=50, default='standard')
    
    # Inheritance - nullable FKs for policy overrides
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, null=True, blank=True, related_name='grading_policies')
    programme = models.ForeignKey(Programme, on_delete=models.CASCADE, null=True, blank=True, related_name='grading_policies')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True, related_name='grading_policies')
    institution = models.ForeignKey('institution.InstitutionSettings', on_delete=models.CASCADE, null=True, blank=True, related_name='grading_policies')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'grading_policies'
    
    def __str__(self):
        return self.name
    
    def get_grade_point(self, score):
        """Calculate grade point from score"""
        boundaries = self.get_boundaries()
        
        if score >= boundaries.get('A', 70):
            return self.get_max_grade_point()
        elif score >= boundaries.get('B', 60):
            return self.get_max_grade_point() * 0.8
        elif score >= boundaries.get('C', 50):
            return self.get_max_grade_point() * 0.6
        elif score >= boundaries.get('D', 45):
            return self.get_max_grade_point() * 0.4
        elif score >= boundaries.get('E', 40):
            return self.get_max_grade_point() * 0.2
        return 0.0
    
    def get_grade(self, score):
        """Get letter grade from score"""
        boundaries = self.get_boundaries()
        
        if score >= boundaries.get('A', 70):
            return 'A'
        elif score >= boundaries.get('B', 60):
            return 'B'
        elif score >= boundaries.get('C', 50):
            return 'C'
        elif score >= boundaries.get('D', 45):
            return 'D'
        elif score >= boundaries.get('E', 40):
            return 'E'
        return 'F'
    
    def get_boundaries(self):
        """Get grade boundaries"""
        if self.grade_boundaries:
            return self.grade_boundaries
        
        if self.scale_type == 'british':
            return {'A': 70, 'B': 60, 'C': 50, 'D': 45, 'E': 40}
        elif self.scale_type == 'american':
            return {'A': 90, 'B': 80, 'C': 70, 'D': 60}
        return {'A': 70, 'B': 60, 'C': 50, 'D': 45, 'E': 40}
    
    def get_max_grade_point(self):
        """Get max grade point based on scale"""
        if self.scale_type == 'british':
            return 5.0
        elif self.scale_type == 'american':
            return 4.0
        return 5.0