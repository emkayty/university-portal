"""Hostel API"""
from ninjaJWT import router as hostel_router

@hostel_router.get('/')
def list_hostel(request):
    from apps.hostel.models import Hostel
    return Hostel.objects.all()[:20]
