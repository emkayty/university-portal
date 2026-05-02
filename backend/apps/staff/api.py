"""Staff API - Staff Management"""
from ninja import Schema
from ninjaJWT import router as staff_router


class StaffProfileSchema(Schema):
    id: str
    staff_id: str
    first_name: str
    last_name: str
    department_id: str = ''
    rank: str


# Staff endpoints
@staff_router.get('/staff', response=list[StaffProfileSchema])
def list_staff(request, department_id: str = None):
    """List staff members"""
    from apps.staff.models import StaffProfile
    query = StaffProfile.objects.all()
    if department_id:
        query = query.filter(department_id=department_id)
    return query


@staff_router.get('/staff/me', response=StaffProfileSchema)
def get_my_profile(request):
    """Get current staff profile"""
    from apps.staff.models import StaffProfile
    profile = StaffProfile.objects.get(user=request.user)
    return profile


# Leave endpoints
@staff_router.post('/leave')
def request_leave(request, leave_type: str, start_date: str, end_date: str, reason: str):
    """Request leave"""
    from apps.staff.models import LeaveRequest, StaffProfile
    from datetime import datetime
    
    profile = StaffProfile.objects.get(user=request.user)
    leave = LeaveRequest.objects.create(
        staff=profile,
        leave_type=leave_type,
        start_date=datetime.strptime(start_date, '%Y-%m-%d').date(),
        end_date=datetime.strptime(end_date, '%Y-%m-%d').date(),
        reason=reason
    )
    return leave


@staff_router.get('/leave', response=list)
def list_leave_requests(request, status: str = None):
    """List leave requests"""
    from apps.staff.models import LeaveRequest, StaffProfile
    
    profile = StaffProfile.objects.get(user=request.user)
    query = LeaveRequest.objects.filter(staff=profile)
    if status:
        query = query.filter(status=status)
    return query


# Payroll endpoints (Bursar only)
@staff_router.get('/payroll')
def get_payroll(request, month: str = None):
    """Get payroll records"""
    from apps.finance.models import PayrollRecord
    from apps.accounts.models import User
    
    if not request.user.has_role('bursar', 'institution_admin'):
        return 403, {'error': 'Access denied'}
    
    query = PayrollRecord.objects.all()
    if month:
        query = query.filter(month=month)
    return query