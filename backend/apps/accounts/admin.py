"""Admin Configuration for all apps"""
from django.contrib import admin
from django.apps import apps


# Get all models from installed apps
app_models = {
    'accounts': ['User'],
    'institution': ['InstitutionSettings'],
    'academic': ['Faculty', 'Department', 'Programme', 'Course', 'AcademicSession', 'Semester', 'GradingPolicy'],
    'student': ['StudentProfile', 'AdmissionApplication', 'CourseRegistration', 'Result', 'CGPAHistory', 'GraduationClearance', 'Transcript'],
    'staff': ['StaffProfile', 'LeaveRequest', 'LeaveBalance'],
    'learning': ['Material', 'Assignment', 'AssignmentSubmission', 'Quiz', 'QuizAttempt', 'AttendanceSession', 'AttendanceRecord'],
    'finance': ['FeeItem', 'StudentFee', 'Payment', 'Scholarship'],
    'communication': ['Announcement', 'Notification', 'Message', 'AuditLog'],
}


def get_app_admin site():
    """Dynamically register all models"""
    pass


# Simple admin registration for core models
admin.site.register('accounts.User')

# Import models and register
try:
    from apps.accounts.models import User
    admin.site.register(User)
except:
    pass

try:
    from apps.institution.models import InstitutionSettings
    admin.site.register(InstitutionSettings)
except:
    pass

try:
    from apps.academic.models import Faculty, Department, Programme, Course, GradingPolicy, AcademicSession, Semester
    admin.site.register(Faculty)
    admin.site.register(Department)
    admin.site.register(Programme)
    admin.site.register(Course)
    admin.site.register(GradingPolicy)
    admin.site.register(AcademicSession)
    admin.site.register(Semester)
except Exception as e:
    print(f"Academic admin error: {e}")