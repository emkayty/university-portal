"""Health API"""
from ninjaJWT import router as health_router

@health_router.get('/')
def list_health(request):
    from apps.health.models import Health
    return Health.objects.all()[:20]
