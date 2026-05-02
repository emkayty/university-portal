"""Institution API - Settings & Setup Wizard"""
from ninja import Schema
from ninjaJWT import router as institution_router


class SettingsSchema(Schema):
    id: str
    institution_name: str
    motto: str = ''
    logo_url: str = ''
    primary_color: str = '#1e40af'
    secondary_color: str = '#059669'
    grading_scale_type: str = 'british'
    academic_year_start: str


class SettingsUpdateSchema(Schema):
    institution_name: str
    motto: str = ''
    primary_color: str = '#1e40af'
    secondary_color: str = '#059669'
    grading_scale_type: str = 'british'


@institution_router.get('/settings', response=SettingsSchema)
def get_settings(request):
    from apps.institution.models import InstitutionSettings
    
    settings = InstitutionSettings.objects.first()
    if not settings:
        return {'error': 'Setup not complete'}, 404
    
    return settings


@institution_router.patch('/settings', response=SettingsSchema)
def update_settings(request, data: SettingsUpdateSchema):
    from apps.institution.models import InstitutionSettings
    
    settings = InstitutionSettings.objects.first()
    if not settings:
        return {'error': 'Settings not found'}, 404
    
    for key, value in data.dict().items():
        if value is not None:
            setattr(settings, key, value)
    
    settings.save()
    return settings


@institution_router.post('/setup')
def complete_setup(request):
    """Complete setup wizard - first time setup"""
    from apps.institution.models import InstitutionSettings
    from apps.accounts.models import User
    
    # Check if setup already complete
    if InstitutionSettings.objects.exists():
        return 400, {'error': 'Setup already complete'}
    
    return {'message': 'Setup wizard endpoint ready'}