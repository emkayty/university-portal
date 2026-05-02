"""Complaint API"""
from ninjaJWT import router as complaint_router
@complaint_router.get('/')
def list_complaints(request):
    from apps.complaint.models import Complaint
    return Complaint.objects.all()[:20]
