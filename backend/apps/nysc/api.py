"""NYSC API"""
from ninja import Schema
from ninjaJWT import router as nysc_router

@nysc_router.get('/profile/')
def get_nysc_profile(request):
    from apps.nysc.models import NYSCProfile
    from apps.student.models import StudentProfile
    profile = StudentProfile.objects.get(user=request.user)
    return NYSCProfile.objects.filter(student=profile).first()

@nysc_router.get('/batches/')
def list_batches(request):
    from apps.nysc.models import NYSCBatch
    return NYSCBatch.objects.filter(is_active=True)[:10]
