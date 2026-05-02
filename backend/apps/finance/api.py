"""Finance API - Fees, Payments"""
from ninja import Schema
from ninjaJWT import router as finance_router


class FeeItemSchema(Schema):
    id: str
    name: str
    amount: float
    is_compulsory: bool
    programme_id: str = ''
    level: int


class PaymentSchema(Schema):
    id: str
    amount: float
    payment_ref: str
    gateway: str
    status: str


# Fee endpoints
@finance_router.get('/fees', response=list[FeeItemSchema])
def list_fees(request, programme_id: str = None, level: int = None):
    """List fee items"""
    from apps.finance.models import FeeItem
    query = FeeItem.objects.all()
    if programme_id:
        query = query.filter(programme_id=programme_id)
    if level:
        query = query.filter(level=level)
    return query


@finance_router.get('/fees/student/{student_id}')
def get_student_fees(request, student_id: str):
    """Get student fees"""
    from apps.finance.models import StudentFee
    from apps.accounts.models import User
    
    fees = StudentFee.objects.filter(student_id=student_id)
    return [{
        'id': str(f.id),
        'fee_item': f.fee_item.name,
        'amount_due': float(f.amount_due),
        'amount_paid': float(f.amount_paid),
        'balance': float(f.balance),
        'status': f.status
    } for f in fees]


# Payment endpoints
@finance_router.post('/payments/initialize')
def initialize_payment(request, amount: float, fee_item_ids: list[str]):
    """Initialize payment with gateway"""
    from apps.finance.models import Payment, StudentFee
    from apps.accounts.models import User
    from apps.institution.models import InstitutionSettings
    from datetime import datetime
    import secrets
    
    # Get settings
    settings = InstitutionSettings.objects.first()
    gateway = settings.payment_gateway if settings else 'paystack'
    
    # Create payment
    ref = f"{gateway.upper()}{datetime.now().strftime('%Y%m%d%H%M%S')}{secrets.token_hex(4)}"
    payment = Payment.objects.create(
        student=request.user,
        amount=amount,
        payment_ref=ref,
        gateway=gateway
    )
    
    return {
        'payment_ref': ref,
        'amount': amount,
        'gateway': gateway,
        'access_code': 'mock_access_code',  # Would call gateway API in production
        'authorization_url': f'https://{gateway}.mock/pay/{ref}'
    }


@finance_router.get('/payments/verify')
def verify_payment(request, reference: str):
    """Verify payment status"""
    from apps.finance.models import Payment
    
    payment = Payment.objects.get(payment_ref=reference)
    
    # Would verify with gateway in production
    payment.status = 'success'
    payment.paid_at = datetime.now()
    payment.save()
    
    return payment


@finance_router.get('/payments/history', response=list[PaymentSchema])
def payment_history(request):
    """Get payment history"""
    from apps.finance.models import Payment
    return Payment.objects.filter(student=request.user)


# Scholarship endpoints
@finance_router.get('/scholarships', response=list)
def list_scholarships(request):
    """List scholarships"""
    from apps.finance.models import Scholarship
    from apps.accounts import User
    
    if not request.user.has_role('bursar', 'institution_admin'):
        return 403, {'error': 'Access denied'}
    return Scholarship.objects.all()