"""Calendar API"""
from ninjaJWT import router as calendar_router
@calendar_router.get('/')
def list_calendars(request):
    from apps.calendar.models import Calendar
    return Calendar.objects.all()[:20]
