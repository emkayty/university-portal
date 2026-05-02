"""Reports API - Analytics & Transcripts"""
from django.db import models
from ninja import Schema
from ninjaJWT import router as reports_router


class TranscriptRequestSchema(Schema):
    student_id: str
    purpose: str


class TranscriptResponseSchema(Schema):
    transcript_id: str
    student_name: str
    issued_at: str
    pdf_url: str
    qr_code: str


class AnalyticsSchema(Schema):
    total_students: int
    total_staff: int
    active_courses: int
    average_gpa: float
    graduation_rate: float


@reports_router.post('/transcript/request', response=TranscriptResponseSchema)
def request_transcript(request, data: TranscriptRequestSchema):
    """Request official transcript"""
    from apps.student.models import Transcript, StudentProfile
    import uuid
    
    try:
        student = StudentProfile.objects.get(id=data.student_id)
        qr_code = f"TR-{uuid.uuid4().hex[:12].upper()}"
        
        transcript = Transcript.objects.create(
            student=student,
            qr_verification_code=qr_code
        )
        
        return {
            'transcript_id': str(transcript.id),
            'student_name': student.full_name,
            'issued_at': str(transcript.issued_at),
            'pdf_url': transcript.pdf_url,
            'qr_code': qr_code
        }
    except StudentProfile.DoesNotExist:
        return 404, {'error': 'Student not found'}


@reports_router.get('/analytics', response=AnalyticsSchema)
def get_analytics(request):
    """Get system analytics"""
    from apps.student.models import StudentProfile
    from apps.staff.models import StaffProfile
    from apps.learning.models import Course
    from apps.student.models import CGPAHistory
    
    total_students = StudentProfile.objects.filter(admission_status='admitted').count()
    total_staff = StaffProfile.objects.count()
    active_courses = Course.objects.filter(is_active=True).count()
    
    avg_gpa = CGPAHistory.objects.aggregate(models.Avg('cumulative_gpa'))
    average_gpa = float(avg_gpa['cumulative_gpa__avg'] or 0.0)
    
    graduated = StudentProfile.objects.filter(admission_status='graduated').count()
    graduation_rate = (graduated / total_students * 100) if total_students > 0 else 0
    
    return {
        'total_students': total_students,
        'total_staff': total_staff,
        'active_courses': active_courses,
        'average_gpa': round(average_gpa, 2),
        'graduation_rate': round(graduation_rate, 2)
    }


@reports_router.get('/student/{student_id}/history')
def get_student_history(request, student_id: str):
    """Get student academic history"""
    from apps.student.models import StudentProfile, CGPAHistory, Result
    
    try:
        student = StudentProfile.objects.get(id=student_id)
        cgpahistory = CGPAHistory.objects.filter(student=student)
        results = Result.objects.filter(registration__student=student)
        
        return {
            'student': student.full_name,
            'cgpa_history': list(cgpahistory.values('session', 'semester', 'gpa', 'cumulative_gpa')),
            'results': list(results.values('registration__course', 'score', 'grade', 'status'))
        }
    except StudentProfile.DoesNotExist:
        return 404, {'error': 'Student not found'}