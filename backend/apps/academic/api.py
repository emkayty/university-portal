"""Academic API - Academic Structure"""
from ninja import Schema
from typing import Optional
from ninjaJWT import router as academic_router


class FacultySchema(Schema):
    id: str
    name: str
    code: str


class DepartmentSchema(Schema):
    id: str
    name: str
    code: str
    faculty_id: str


class ProgrammeSchema(Schema):
    id: str
    name: str
    code: str
    department_id: str
    duration_years: int


class CourseSchema(Schema):
    id: str
    code: str
    title: str
    credit_units: int
    level: int
    semester_offered: int
    programme_id: str
    department_id: str


class GradingPolicySchema(Schema):
    id: str
    name: str
    scale_type: str
    grade_boundaries: dict
    pass_mark: int
    max_score: int


class SessionSchema(Schema):
    id: str
    name: str
    start_date: str
    end_date: str
    is_current: bool


class SemesterSchema(Schema):
    id: str
    session_id: str
    name: str
    start_date: str
    end_date: str
    registration_start: str
    registration_end: str


# Faculty endpoints
@academic_router.get('/faculties', response=list[FacultySchema])
def list_faculties(request):
    from apps.academic.models import Faculty
    return Faculty.objects.all()


@academic_router.post('/faculties', response=FacultySchema)
def create_faculty(request, name: str, code: str):
    from apps.academic.models import Faculty
    faculty = Faculty.objects.create(name=name, code=code)
    return faculty


# Department endpoints
@academic_router.get('/departments', response=list[DepartmentSchema])
def list_departments(request, faculty_id: str = None):
    from apps.academic.models import Department
    query = Department.objects.all()
    if faculty_id:
        query = query.filter(faculty_id=faculty_id)
    return query


# Programme endpoints
@academic_router.get('/programmes', response=list[ProgrammeSchema])
def list_programmes(request, department_id: str = None):
    from apps.academic.models import Programme
    query = Programme.objects.all()
    if department_id:
        query = query.filter(department_id=department_id)
    return query


# Course endpoints
@academic_router.get('/courses', response=list[CourseSchema])
def list_courses(request, programme_id: str = None, level: int = None):
    from apps.academic.models import Course
    query = Course.objects.all()
    if programme_id:
        query = query.filter(programme_id=programme_id)
    if level:
        query = query.filter(level=level)
    return query


# Grading Policy endpoints
@academic_router.get('/grading-policies', response=list[GradingPolicySchema])
def list_grading_policies(request, faculty_id: str = None):
    from apps.academic.models import GradingPolicy
    query = GradingPolicy.objects.all()
    if faculty_id:
        query = query.filter(faculty_id=faculty_id)
    return query


@academic_router.get('/grading-policies/resolve')
def resolve_grading_policy(request, course_id: str = None, programme_id: str = None):
    from utils.grading import resolve_grading_policy
    from apps.institution.models import InstitutionSettings
    
    institution = InstitutionSettings.objects.first()
    policy = resolve_grading_policy(
        course_id=course_id,
        programme_id=programme_id,
        institution_default=institution
    )
    
    if policy:
        return {
            'id': str(policy.id),
            'name': policy.name,
            'scale_type': policy.scale_type,
            'grade_boundaries': policy.get_boundaries(),
            'pass_mark': policy.pass_mark,
            'max_score': policy.max_score
        }
    return {'error': 'No policy found'}


# Session endpoints
@academic_router.get('/sessions', response=list[SessionSchema])
def list_sessions(request):
    from apps.academic.models import AcademicSession
    return AcademicSession.objects.all()


@academic_router.get('/sessions/current')
def get_current_session(request):
    from apps.academic.models import AcademicSession
    session = AcademicSession.objects.filter(is_current=True).first()
    if not session:
        return {'error': 'No current session'}
    return session


# Semester endpoints
@academic_router.get('/semesters', response=list[SemesterSchema])
def list_semesters(request, session_id: str = None):
    from apps.academic.models import Semester
    query = Semester.objects.all()
    if session_id:
        query = query.filter(session_id=session_id)
    return query