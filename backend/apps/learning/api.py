"""Learning API - Materials, Assignments, Quizzes, Attendance"""
from ninja import Schema
from ninjaJWT import router as learning_router


class MaterialSchema(Schema):
    id: str
    course_id: str
    title: str
    file_url: str
    type: str
    is_offline_available: bool


class AssignmentSchema(Schema):
    id: str
    course_id: str
    title: str
    description: str
    due_date: str
    max_score: float


class QuizSchema(Schema):
    id: str
    course_id: str
    title: str
    duration_minutes: int
    start_time: str
    end_time: str


class AttendanceSessionSchema(Schema):
    id: str
    course_id: str
    date: str
    qr_code_token: str
    is_active: bool


# Materials endpoints
@learning_router.get('/materials', response=list[MaterialSchema])
def list_materials(request, course_id: str = None):
    """List learning materials"""
    from apps.learning.models import Material
    query = Material.objects.all()
    if course_id:
        query = query.filter(course_id=course_id)
    return query


@learning_router.post('/materials')
def upload_material(request, course_id: str, title: str, file_url: str, type: str = 'pdf'):
    """Upload material"""
    from apps.learning.models import Material
    from apps.academic.models import Course
    
    course = Course.objects.get(id=course_id)
    material = Material.objects.create(
        course=course,
        lecturer=request.user,
        title=title,
        file_url=file_url,
        type=type
    )
    return material


# Assignments endpoints
@learning_router.get('/assignments', response=list[AssignmentSchema])
def list_assignments(request, course_id: str = None):
    """List assignments"""
    from apps.learning.models import Assignment
    query = Assignment.objects.all()
    if course_id:
        query = query.filter(course_id=course_id)
    return query


@learning_router.post('/assignments')
def create_assignment(request, course_id: str, title: str, description: str, due_date: str, max_score: float = 100):
    """Create assignment"""
    from apps.learning.models import Assignment
    from apps.academic.models import Course
    from datetime import datetime
    
    course = Course.objects.get(id=course_id)
    assignment = Assignment.objects.create(
        course=course,
        lecturer=request.user,
        title=title,
        description=description,
        due_date=datetime.fromisoformat(due_date),
        max_score=max_score
    )
    return assignment


@learning_router.post('/assignments/{assignment_id}/submit')
def submit_assignment(request, assignment_id: str, file_url: str = None, text_answer: str = None):
    """Submit assignment"""
    from apps.learning.models import AssignmentSubmission, Assignment
    from apps.accounts.models import User
    from datetime import datetime
    
    assignment = Assignment.objects.get(id=assignment_id)
    submission, _ = AssignmentSubmission.objects.get_or_create(
        assignment=assignment,
        student=request.user
    )
    submission.file_url = file_url
    submission.text_answer = text_answer
    submission.submitted_at = datetime.now()
    submission.status = 'submitted'
    submission.save()
    return submission


# Quizzes endpoints
@learning_router.get('/quizzes', response=list[QuizSchema])
def list_quizzes(request, course_id: str = None):
    """List quizzes"""
    from apps.learning.models import Quiz
    query = Quiz.objects.all()
    if course_id:
        query = query.filter(course_id=course_id)
    return query


@learning_router.post('/quizzes')
def create_quiz(request, course_id: str, title: str, duration_minutes: int, 
            start_time: str, end_time: str, questions: list):
    """Create quiz"""
    from apps.learning.models import Quiz
    from apps.academic.models import Course
    from datetime import datetime
    
    course = Course.objects.get(id=course_id)
    quiz = Quiz.objects.create(
        course=course,
        lecturer=request.user,
        title=title,
        duration_minutes=duration_minutes,
        start_time=datetime.fromisoformat(start_time),
        end_time=datetime.fromisoformat(end_time),
        questions=questions
    )
    return quiz


@learning_router.post('/quizzes/{quiz_id}/start')
def start_quiz(request, quiz_id: str):
    """Start quiz attempt"""
    from apps.learning.models import QuizAttempt, Quiz
    from datetime import datetime
    
    quiz = Quiz.objects.get(id=quiz_id)
    attempt = QuizAttempt.objects.create(
        quiz=quiz,
        student=request.user,
        started_at=datetime.now()
    )
    return attempt


@learning_router.post('/quizzes/{quiz_id}/submit')
def submit_quiz_attempt(request, quiz_id: str, attempt_id: str, answers: dict):
    """Submit quiz attempt"""
    from apps.learning.models import QuizAttempt, Quiz
    from apps.academic.models import Course
    from utils.grading import calculate_grade_point
    
    quiz = Quiz.objects.get(id=quiz_id)
    attempt = QuizAttempt.objects.get(id=attempt_id, quiz=quiz)
    attempt.answers = answers
    attempt.submitted_at = datetime.now()
    
    # Auto-grade (simplified)
    score = 0
    for q in quiz.questions or []:
        if answers.get(str(q.get('id'))) == q.get('correct_answer'):
            score += 1
    
    max_score = len(quiz.questions) if quiz.questions else 1
    attempt.score_total = (score / max_score) * 100
    attempt.save()
    
    return attempt


# Attendance endpoints
@learning_router.get('/attendance/sessions', response=list[AttendanceSessionSchema])
def list_attendance_sessions(request, course_id: str = None):
    """List attendance sessions"""
    from apps.learning.models import AttendanceSession
    query = AttendanceSession.objects.all()
    if course_id:
        query = query.filter(course_id=course_id)
    return query


@learning_router.post('/attendance/sessions')
def create_attendance_session(request, course_id: str, date: str):
    """Create attendance session"""
    from apps.learning.models import AttendanceSession
    from apps.academic.models import Course
    from datetime import datetime
    import secrets
    
    course = Course.objects.get(id=course_id)
    session = AttendanceSession.objects.create(
        course=course,
        lecturer=request.user,
        date=datetime.strptime(date, '%Y-%m-%d').date(),
        qr_code_token=secrets.token_urlsafe(16)
    )
    return session


@learning_router.post('/attendance/sessions/{session_id}/record')
def record_attendance(request, session_id: str, method: str = 'qr'):
    """Record attendance (QR scan or manual)"""
    from apps.learning.models import AttendanceRecord, AttendanceSession
    
    session = AttendanceSession.objects.get(id=session_id)
    record = AttendanceRecord.objects.create(
        attendance_session=session,
        student=request.user,
        method=method
    )
    return record


# Grade submission (Lecturer)
@learning_router.post('/grades')
def submit_grade_sheet(request, course_id: str, semester_id: str, results: list):
    """Submit grade sheet for approval"""
    from apps.student.models import CourseRegistration, Result
    from apps.academic.models import Course, Semester
    from utils.grading import calculate_grade_point, resolve_grading_policy
    
    course = Course.objects.get(id=course_id)
    semester = Semester.objects.get(id=semester_id)
    
    # Get policy
    policy = resolve_grading_policy(
        course_id=str(course.id),
        programme_id=str(course.programme.id) if course.programme else None
    )
    
    created = []
    for r in results:
        reg = CourseRegistration.objects.get(id=r.get('registration_id'))
        
        score = float(r.get('score'))
        grade = policy.get_grade(score)
        grade_point = calculate_grade_point(score, policy)
        
        result, _ = Result.objects.update_or_create(
            registration=reg,
            session=semester.session,
            semester=semester,
            defaults={
                'score': score,
                'grade': grade,
                'grade_point': grade_point,
                'lecturer': request.user,
                'status': 'pending'
            }
        )
        created.append(result)
    
    return created