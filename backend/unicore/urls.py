"""URL Configuration"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from ninja import NinjaAPI
from apps.accounts.api import router as accounts_router
from apps.institution.api import router as institution_router
from apps.academic.api import router as academic_router
from apps.student.api import router as student_router
from apps.staff.api import router as staff_router
from apps.learning.api import router as learning_router
from apps.finance.api import router as finance_router
from apps.communication.api import router as communication_router
from apps.offline.api import router as offline_router

api = NinjaAPI()

# Mount all API routers
api.add_router('/auth/', accounts_router, tags=['auth'])
api.add_router('/settings/', institution_router, tags=['settings'])
api.add_router('/academic/', academic_router, tags=['academic'])
api.add_router('/students/', student_router, tags=['students'])
api.add_router('/staff/', staff_router, tags=['staff'])
api.add_router('/learning/', learning_router, tags=['learning'])
api.add_router('/finance/', finance_router, tags=['finance'])
api.add_router('/communication/', communication_router, tags=['communication'])
api.add_router('/offline/', offline_router, tags=['offline'])

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', api.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)