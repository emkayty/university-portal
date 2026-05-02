"""Library API"""
from ninjaJWT import router as lib_router
@lib_router.get('/borrowed/')
def get_borrowed(request):
    from apps.library.models import BookIssue
    from apps.student.models import StudentProfile
    profile = StudentProfile.objects.get(user=request.user)
    return BookIssue.objects.filter(student=profile, status='issued')
