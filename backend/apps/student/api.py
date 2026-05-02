"""Student API - Student Management"""
from ninja import Schema
from typing import Optional
from ninjaJWT import router as student_router


class StudentProfileSchema(Schema):
    id: str
    user_id: str
    matric_number: Optional[str]
    first_name: str
    last_name: str
    gender: str
    phone: str = ''
    programme_id: Optional[str]
    current_level: int
    admission_status: str


class AdmissionApplicationSchema(Schema):
    id: str
    student_profile_id: str
    jamb_reg_no: str = ''
    jamb_score: Optional[int]
    application_session_id: str
    status: str


class RegistrationSchema(Schema):
    id: str
    course_id: str
    session_id: str
    semester_id: str
    status: str


class ResultSchema(Schema):
    id: str
    registration_id: str
    course_code: str
    course_title: str
    score: float
    grade: str
    grade_point: float
    status: str
    session_name: str
    semester_name: str


# Admission endpoints
@student_router.post('/admissions/apply')
def apply_admission(request, jamb_reg_no: str = None, jamb_score: int = None):
    """Submit admission application"""
    from apps.student.models import AdmissionApplication, StudentProfile
    from apps.academic.models import AcademicSession
    
    # Get current session
    session = AcademicSession.objects.filter(is_current=True).first()
    if not session:
        return 400, {'error': 'No active admission session'}
    
    # Create application with current user as student
    profile = StudentProfile.objects.get(user=request.user)
    
    application = AdmissionApplication.objects.create(
        student_profile=profile,
        jamb_reg_no=jamb_reg_no,
        jamb_score=jamb_score,
        application_session=session
    )
    
    return application


@student_router.get('/admissions/applications')
def list_applications(request, status: str = None):
    """List admission applications (for registrar)"""
    from apps.student.models import AdmissionApplication
    query = AdmissionApplication.objects.all()
    if status:
        query = query.filter(status=status)
    return query


# Student endpoints
@student_router.get('/students/me', response=StudentProfileSchema)
def get_my_profile(request):
    """Get current student profile"""
    from apps.student.models import StudentProfile
    profile = StudentProfile.objects.get(user=request.user)
    return profile


@student_router.get('/students/{student_id}', response=StudentProfileSchema)
def get_student(request, student_id: str):
    """Get student by ID (for staff)"""
    from apps.student.models import StudentProfile
    profile = StudentProfile.objects.get(id=student_id)
    return profile


# Registration endpoints
@student_router.get('/registrations', response=list[RegistrationSchema])
def list_registrations(request, semester_id: str = None):
    """List student course registrations"""
    from apps.student.models import CourseRegistration
    from apps.academic.models import Semester
    
    query = CourseRegistration.objects.filter(student__user=request.user)
    if semester_id:
        query = query.filter(semester_id=semester_id)
    return query


@student_router.post('/registrations')
def register_courses(request, course_ids: list[str], semester_id: str):
    """Register for courses"""
    from apps.student.models import CourseRegistration
    from apps.student.models import StudentProfile
    from apps.academic.models import Course, Semester
    from utils.grading import has_timetable_clash
    
    profile = StudentProfile.objects.get(user=request.user)
    semester = Semester.objects.get(id=semester_id)
    
    registered = []
    errors = []
    
    for course_id in course_ids:
        course = Course.objects.get(id=course_id)
        
        # Check for timetable clash
        if has_timetable_clash(profile, course, semester):
            errors.append(f"{course.code}: Timetable clash")
            continue
        
        # Check if already registered
        if CourseRegistration.objects.filter(
            student=profile,
            course=course,
            semester=semester
        ).exists():
            errors.append(f"{course.code}: Already registered")
            continue
        
        reg = CourseRegistration.objects.create(
            student=profile,
            course=course,
            session=semester.session,
            semester=semester
        )
        registered.append(reg)
    
    return {
        'registered': registered,
        'errors': errors
    }


# Results endpoints
@student_router.get('/results')
def get_results(request, semester_id: str = None):
    """Get student results"""
    from apps.student.models import Result, CourseRegistration
    from apps.student.models import StudentProfile
    
    profile = StudentProfile.objects.get(user=request.user)
    query = Result.objects.filter(
        registration__student=profile,
        status='approved'
    )
    
    if semester_id:
        query = query.filter(semester_id=semester_id)
    
    results = []
    for r in query:
        results.append({
            'id': str(r.id),
            'registration_id': str(r.registration_id),
            'course_code': r.registration.course.code,
            'course_title': r.registration.course.title,
            'score': float(r.score),
            'grade': r.grade,
            'grade_point': float(r.grade_point),
            'status': r.status,
            'session_name': r.session.name,
            'semester_name': r.semester.name
        })
    
    return results


@student_router.get('/cgpa')
def get_cgpa(request):
    """Get current CGPA"""
    from apps.student.models import StudentProfile
    from utils.grading import calculate_cgpa
    
    profile = StudentProfile.objects.get(user=request.user)
    cgpa = calculate_cgpa(profile)
    
    return {'cgpa': cgpa}


# Clearance endpoints
@student_router.get('/clearance')
def get_clearance(request):
    """Get graduation clearance status"""
    from apps.student.models import StudentProfile, GraduationClearance
    
    profile = StudentProfile.objects.get(user=request.user)
    clearance = getattr(profile, 'graduation_clearance', None)
    
    if not clearance:
        return {'error': 'Clearance not initiated'}
    
    return {
        'library': clearance.cleared_by_library,
        'hostel': clearance.cleared_by_hostel,
        'bursary': clearance.cleared_by_bursary,
        'department': clearance.cleared_by_department,
        'progress': clearance.progress,
        'eligible': clearance.eligible_to_graduate
    }