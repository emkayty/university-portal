"""
from django.db import models
Finance API - REAL endpoints
==================================
"""
from ninja import Schema
from typing import Optional
from ninjaJWT import router as finance_router


class FeeSchema(Schema):
    id: str
    name: str
    amount: float
    amount_paid: float
    is_paid: bool
    due_date: str


class PaymentSchema(Schema):
    id: str
    amount: float
    payment_type: str
    status: str
    created_at: str


# Student fees
@finance_router.get('/fees/', response=list[FeeSchema])
def list_my_fees(request):
    """Get student's fee records"""
    from apps.finance.models import StudentFee
    from apps.student.models import StudentProfile
    
    profile = StudentProfile.objects.get(user=request.user)
    return StudentFee.objects.filter(student=profile)


@finance_router.get('/fees/summary')
def get_fee_summary(request):
    """Get fee summary"""
    from apps.finance.models import StudentFee
    from apps.student.models import StudentProfile
    
    profile = StudentProfile.objects.get(user=request.user)
    fees = StudentFee.objects.filter(student=profile)
    
    total = fees.aggregate(total=models.Sum('amount'))['total'] or 0
    paid = fees.aggregate(paid=models.Sum('amount_paid'))['paid'] or 0
    balance = total - paid
    
    return {
        'total': float(total),
        'paid': float(paid),
        'balance': float(balance),
        'is_clear': balance <= 0
    }


# Make payment
@finance_router.post('/payments/initialize')
def initialize_payment(request, amount: float, fee_ids: list[str]):
    """Initialize payment"""
    from apps.finance.models import Payment, StudentFee
    from apps.student.models import StudentProfile
    
    profile = StudentProfile.objects.get(user=request.user)
    
    # Create payment record
    payment = Payment.objects.create(
        student=profile,
        amount=amount,
        payment_type='school_fees',
        status='pending'
    )
    
    return {
        'payment_id': str(payment.id),
        'amount': amount,
        'reference': f'PAY-{payment.id}',
        'instructions': 'Use reference to pay via bank'
    }


# All fees (admin/bursar)
@finance_router.get('/all-fees/', response=list[FeeSchema])
def list_all_fees(request, status: str = None):
    """List all fee records"""
    from apps.finance.models import StudentFee
    
    query = StudentFee.objects.all()
    if status == 'paid':
        query = query.filter(is_paid=True)
    elif status == 'unpaid':
        query = query.filter(is_paid=False)
    
    return query[:100]


# All payments (admin/bursar)
@finance_router.get('/all-payments/', response=list[PaymentSchema])
def list_all_payments(request):
    """List all payments"""
    from apps.finance.models import Payment
    
    return Payment.objects.order_by('-created_at')[:100]


# Revenue analytics
@finance_router.get('/revenue/')
def get_revenue(request):
    """Get revenue analytics"""
    from apps.finance.models import Payment
    from django.db.models import Sum
    
    completed = Payment.objects.filter(status='completed')
    
    total = completed.aggregate(total=Sum('amount'))['total'] or 0
    
    by_type = completed.values('payment_type').annotate(total=Sum('amount'))
    
    return {
        'total_revenue': float(total),
        'by_type': list(by_type)
    }
