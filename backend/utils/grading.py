"""Grading Policy Resolution & CGPA Calculator"""
from decimal import Decimal
from typing import Optional
from apps.academic.models import GradingPolicy, Course, Programme, Faculty


def resolve_grading_policy(
    course_id: Optional[str] = None,
    programme_id: Optional[str] = None,
    faculty_id: Optional[str] = None,
    institution_default: Optional[GradingPolicy] = None
) -> GradingPolicy:
    """
    Resolve effective grading policy with inheritance:
    1. Course-specific policy
    2. Programme-specific policy
    3. Faculty-specific policy
    4. Institution default
    """
    # Try course-specific
    if course_id:
        policy = GradingPolicy.objects.filter(course_id=course_id).first()
        if policy:
            return policy
    
    # Try programme-specific
    if programme_id:
        policy = GradingPolicy.objects.filter(programme_id=programme_id).first()
        if policy:
            return policy
    
    # Try faculty-specific
    if faculty_id:
        policy = GradingPolicy.objects.filter(faculty_id=faculty_id).first()
        if policy:
            return policy
    
    # Return institution default or create one
    if institution_default:
        return institution_default
    
    # Create default British/Nigerian policy
    return GradingPolicy.objects.filter(
        scale_type='british',
        faculty__isnull=True,
        programme__isnull=True,
        course__isnull=True,
        institution__isnull=False
    ).first() or GradingPolicy(
        name='Default British',
        scale_type='british',
        grade_boundaries={'A': 70, 'B': 60, 'C': 50, 'D': 45, 'E': 40},
        pass_mark=40,
        max_score=100,
        cgpa_formula='standard'
    )


def calculate_grade_point(score: float, policy: GradingPolicy) -> float:
    """Calculate grade point from score using policy"""
    boundaries = policy.get_boundaries()
    
    if score >= boundaries.get('A', 70):
        return policy.get_max_grade_point()
    elif score >= boundaries.get('B', 60):
        return policy.get_max_grade_point() * 0.8
    elif score >= boundaries.get('C', 50):
        return policy.get_max_grade_point() * 0.6
    elif score >= boundaries.get('D', 45):
        return policy.get_max_grade_point() * 0.4
    elif score >= boundaries.get('E', 40):
        return policy.get_max_grade_point() * 0.2
    return 0.0


def calculate_cgpa(student, session_id: Optional[str] = None) -> float:
    """Calculate CGPA for a student"""
    from apps.student.models import Result, CourseRegistration
    from apps.academic.models import Semester
    
    # Get all approved results
    query = Result.objects.filter(
        registration__student=student,
        status='approved'
    )
    
    if session_id:
        query = query.filter(session_id=session_id)
    
    results = query.select_related('registration__course')
    
    total_grade_points = Decimal('0')
    total_credit_units = 0
    
    for result in results:
        course = result.registration.course
        credit_units = course.credit_units
        
        # Get effective grading policy
        policy = resolve_grading_policy(
            course_id=str(course.id),
            programme_id=str(course.programme.id) if course.programme else None,
            faculty_id=str(course.department.faculty.id) if course.department else None
        )
        
        # Calculate grade point
        grade_point = Decimal(str(calculate_grade_point(float(result.score), policy)))
        
        total_grade_points += grade_point * credit_units
        total_credit_units += credit_units
    
    if total_credit_units == 0:
        return 0.0
    
    return float(total_grade_points / total_credit_units)


def calculate_semester_gpa(student, semester) -> float:
    """Calculate GPA for a specific semester"""
    from apps.student.models import Result
    
    results = Result.objects.filter(
        registration__student=student,
        semester=semester,
        status='approved'
    ).select_related('registration__course')
    
    total_grade_points = Decimal('0')
    total_credit_units = 0
    
    for result in results:
        course = result.registration.course
        credit_units = course.credit_units
        
        # Get effective grading policy
        policy = resolve_grading_policy(
            course_id=str(course.id),
            programme_id=str(course.programme.id) if course.programme else None,
            faculty_id=str(course.department.faculty.id) if course.department else None
        )
        
        grade_point = Decimal(str(calculate_grade_point(float(result.score), policy)))
        
        total_grade_points += grade_point * credit_units
        total_credit_units += credit_units
    
    if total_credit_units == 0:
        return 0.0
    
    return float(total_grade_points / total_credit_units)


def has_timetable_clash(student, new_course, semester) -> bool:
    """Check for timetable clash when adding a new course"""
    from apps.student.models import CourseRegistration, TimetableEntry
    from apps.academic.models import AcademicSession
    
    # Get student's registered courses for the semester
    registrations = CourseRegistration.objects.filter(
        student=student,
        semester=semester,
        status='active'
    ).select_related('course')
    
    # Get new course timetable slots
    new_slots = TimetableEntry.objects.filter(
        course=new_course,
        session=semester.session
    )
    
    for reg in registrations:
        existing_slots = TimetableEntry.objects.filter(
            course=reg.course,
            session=semester.session
        )
        
        for slot in existing_slots:
            for new_slot in new_slots:
                # Check day overlap
                if slot.day_of_week == new_slot.day_of_week:
                    # Check time overlap
                    if (slot.start_time < new_slot.end_time and 
                        new_slot.start_time < slot.end_time):
                        return True
    
    return False


def is_graduation_eligible(student) -> dict:
    """Check graduation eligibility"""
    from apps.student.models import GraduationClearance, Result
    from apps.academic.models import AcademicSession
    
    # Check clearance
    clearance = getattr(student, 'graduation_clearance', None)
    if not clearance:
        return {'eligible': False, 'reason': 'Clearance not initiated'}
    
    if not clearance.eligible_to_graduate:
        return {'eligible': False, 'reason': 'Clearance not completed'}
    
    # Check minimum CGPA (usually 1.0)
    cgpa = calculate_cgpa(student)
    if cgpa < 1.0:
        return {'eligible': False, 'reason': f'CGPA {cgpa} below minimum'}
    
    # Check all required courses passed
    # (simplified - in production check programme requirements)
    
    return {'eligible': True, 'cgpa': cgpa}