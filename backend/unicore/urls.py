"""URL Configuration"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from ninja import NinjaAPI

# Import existing routers
from apps.accounts.api import router as accounts_router
from apps.institution.api import router as institution_router
from apps.academic.api import router as academic_router
from apps.student.api import router as student_router
from apps.staff.api import router as staff_router
from apps.learning.api import router as learning_router
from apps.finance.api import router as finance_router
from apps.communication.api import router as communication_router
from apps.offline.api import router as offline_router
from apps.reports.api import router as reports_router

# Import new routers
try:
    from apps.hostel.api import router as hostel_router
    from apps.health.api import router as health_router
    from apps.nysc.api import router as nysc_router
    from apps.idcard.api import router as idcard_router
    from apps.library.api import router as library_router
    from apps.calendar.api import router as calendar_router
    from apps.complaint.api import router as complaint_router
    from apps.clearance.api import router as clearance_router
    NEW_APPS = True
except ImportError:
    NEW_APPS = False

api = NinjaAPI()

# Mount existing API routers
api.add_router('/auth/', accounts_router, tags=['auth'])
api.add_router('/settings/', institution_router, tags=['settings'])
api.add_router('/academic/', academic_router, tags=['academic'])
api.add_router('/students/', student_router, tags=['students'])
api.add_router('/staff/', staff_router, tags=['staff'])
api.add_router('/learning/', learning_router, tags=['learning'])
api.add_router('/finance/', finance_router, tags=['finance'])
api.add_router('/communication/', communication_router, tags=['communication'])
api.add_router('/offline/', offline_router, tags=['offline'])
api.add_router('/reports/', reports_router, tags=['reports'])

# Mount new API routers (if available)
if NEW_APPS:
    api.add_router('/hostel/', hostel_router, tags=['hostel'])
    api.add_router('/health/', health_router, tags=['health'])
    api.add_router('/nysc/', nysc_router, tags=['nysc'])
    api.add_router('/idcard/', idcard_router, tags=['idcard'])
    api.add_router('/library/', library_router, tags=['library'])
    api.add_router('/calendar/', calendar_router, tags=['calendar'])
    api.add_router('/complaint/', complaint_router, tags=['complaint'])
    api.add_router('/clearance/', clearance_router, tags=['clearance'])

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', api.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)