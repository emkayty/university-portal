"""ID Card API"""
from ninjaJWT import router as idcard_router
@idcard_router.get('/my-card/')
def get_my_card(request):
    from apps.idcard.models import IDCard
    from apps.student.models import StudentProfile
    profile = StudentProfile.objects.get(user=request.user)
    return IDCard.objects.filter(student=profile).first()
@idcard_router.post('/generate/')
def generate_card(request):
    from apps.idcard.models import IDCard
    from apps.student.models import StudentProfile
    import uuid
    profile = StudentProfile.objects.get(user=request.user)
    card = IDCard.objects.get_or_create(student=profile)[0]
    card.card_number = f"UNI-{profile.matric_number or str(uuid.uuid4())[:8]}"
    from datetime import timedelta
    card.expiry_date = ().__class__.__bases__[0].__new__(__import__('datetime')).date.today() + timedelta(days=365)
    card.save()
    return card
