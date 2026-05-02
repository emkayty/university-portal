"""Learning App - Learning Materials, Assignments, Quizzes, Attendance"""
import uuid
from django.db import models
from django.conf import settings
from apps.academic.models import Course, AcademicSession, Semester


class Material(models.Model):
    """Learning Material"""
    
    TYPE_CHOICES = [
        ('pdf', 'PDF Document'),
        ('video', 'Video'),
        ('link', 'External Link'),
        ('document', 'Document'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='materials'
    )
    lecturer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='uploaded_materials'
    )
    title = models.CharField(max_length=255)
    file_url = models.URLField(blank=True)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='pdf')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_offline_available = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'materials'
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return f"{self.course.code} - {self.title}"


class Assignment(models.Model):
    """Assignment"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='assignments'
    )
    lecturer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_assignments'
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateTimeField()
    max_score = models.DecimalField(max_digits=5, decimal_places=2, default=100)
    grading_rubric = models.JSONField(default=dict)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'assignments'
        ordering = ['-due_date']
    
    def __str__(self):
        return f"{self.course.code} - {self.title}"
    
    @property
    def is_past_due(self):
        from django.utils import timezone
        return timezone.now() > self.due_date
    
    @property
    def submission_count(self):
        return self.submissions.count()


class AssignmentSubmission(models.Model):
    """Assignment Submission"""
    
    STATUS_CHOICES = [
        ('not_started', 'Not Started'),
        ('submitted', 'Submitted'),
        ('graded', 'Graded'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    assignment = models.ForeignKey(
        Assignment,
        on_delete=models.CASCADE,
        related_name='submissions'
    )
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='assignment_submissions'
    )
    file_url = models.URLField(blank=True)
    text_answer = models.TextField(blank=True)
    submitted_at = models.DateTimeField(null=True, blank=True)
    score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    feedback = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')
    
    class Meta:
        db_table = 'assignment_submissions'
        unique_together = ['assignment', 'student']
        ordering = ['-submitted_at']
    
    def __str__(self):
        return f"{self.assignment.title} - {self.student.email}"


class Quiz(models.Model):
    """Quiz"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='quizzes'
    )
    lecturer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_quizzes'
    )
    title = models.CharField(max_length=255)
    duration_minutes = models.IntegerField(default=30)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    questions = models.JSONField(default=list)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'quizzes'
        ordering = ['-end_time']
    
    def __str__(self):
        return f"{self.course.code} - {self.title}"
    
    @property
    def is_active(self):
        from django.utils import timezone
        now = timezone.now()
        return self.start_time <= now <= self.end_time
    
    @property
    def question_count(self):
        return len(self.questions) if self.questions else 0


class QuizAttempt(models.Model):
    """Quiz Attempt"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        related_name='attempts'
    )
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='quiz_attempts'
    )
    started_at = models.DateTimeField(auto_now_add=True)
    submitted_at = models.DateTimeField(null=True, blank=True)
    answers = models.JSONField(default=dict)
    score_total = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    class Meta:
        db_table = 'quiz_attempts'
        unique_together = ['quiz', 'student']
        ordering = ['-started_at']
    
    def __str__(self):
        return f"{self.quiz.title} - {self.student.email}"


class AttendanceSession(models.Model):
    """Attendance Session"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='attendance_sessions'
    )
    lecturer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='attendance_sessions'
    )
    date = models.DateField()
    qr_code_token = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'attendance_sessions'
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.course.code} - {self.date}"


class AttendanceRecord(models.Model):
    """Attendance Record"""
    
    METHOD_CHOICES = [
        ('qr', 'QR Code'),
        ('manual', 'Manual'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    attendance_session = models.ForeignKey(
        AttendanceSession,
        on_delete=models.CASCADE,
        related_name='records'
    )
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='attendance_records'
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    method = models.CharField(max_length=10, choices=METHOD_CHOICES, default='qr')
    
    class Meta:
        db_table = 'attendance_records'
        unique_together = ['attendance_session', 'student']
    
    def __str__(self):
        return f"{self.attendance_session.course.code} - {self.student.email}"