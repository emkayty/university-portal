"""Offline API - Offline Sync Endpoints"""
from ninja import Schema
from ninjaJWT import router as offline_router


class AttendanceBatchSchema(Schema):
    session_id: str
    student_id: str
    timestamp: str
    offline_token: str


class OfflineQueueSchema(Schema):
    id: str
    operation_type: str
    created_at: str
    is_synced: bool


# Attendance batch sync
@offline_router.post('/attendance-batch')
def sync_attendance_batch(request, records: list[AttendanceBatchSchema]):
    """Sync attendance records from offline"""
    from apps.learning.models import AttendanceRecord, AttendanceSession
    from datetime import datetime
    
    synced = []
    for r in records:
        session = AttendanceSession.objects.get(id=r.session_id)
        record = AttendanceRecord.objects.get_or_create(
            attendance_session=session,
            student_id=r.student_id,
            defaults={
                'method': 'qr'
            }
        )
        synced.append(record)
    
    return {'synced': len(synced)}


# Assignment offline submit
@offline_router.post('/assignment-submit')
def submit_offline_assignment(request, assignment_id: str, file_data: bytes = None):
    """Submit assignment from offline queue"""
    from apps.learning.models import AssignmentSubmission
    from apps.accounts.models import User
    from datetime import datetime
    
    submission, _ = AssignmentSubmission.objects.get_or_create(
        assignment_id=assignment_id,
        student=request.user
    )
    
    if file_data:
        submission.file_url = 'offline://queued'  # Would upload when online
    submission.submitted_at = datetime.now()
    submission.status = 'submitted'
    submission.save()
    
    return submission


# Sync status
@offline_router.get('/sync-status')
def get_sync_status(request):
    """Get offline sync status"""
    from apps.offline.models import SyncStatus
    
    status, _ = SyncStatus.objects.get_or_create(user=request.user)
    return {
        'last_sync': status.last_sync,
        'pending_count': status.pending_count
    }