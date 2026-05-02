"""Clearance API"""
from ninjaJWT import router as clearance_router
@clearance_router.get('/')
def list_clearances(request):
    from apps.clearance.models import Clearance
    return Clearance.objects.all()[:20]
