"""
Communication API - REAL endpoints
=================================
"""
from ninja import Schema
from typing import Optional
from ninjaJWT import router as comm_router


class NotificationSchema(Schema):
    id: str
    title: str
    message: str
    is_read: bool
    created_at: str


class AnnouncementSchema(Schema):
    id: str
    title: str
    content: str
    priority: str
    target_audience: str
    created_at: str
    expires_at: Optional[str]


# Notifications
@comm_router.get('/notifications/', response=list[NotificationSchema])
def list_notifications(request, unread_only: bool = False):
    """Get user notifications"""
    from apps.communication.models import Notification
    
    query = Notification.objects.filter(user=request.user)
    if unread_only:
        query = query.filter(is_read=False)
    
    return query.order_by('-created_at')[:50]


@comm_router.post('/notifications/{notification_id}/read')
def mark_notification_read(request, notification_id: str):
    """Mark notification as read"""
    from apps.communication.models import Notification
    
    notification = Notification.objects.get(id=notification_id, user=request.user)
    notification.is_read = True
    notification.save()
    return {'success': True}


@comm_router.post('/notifications/read-all')
def mark_all_read(request):
    """Mark all notifications as read"""
    from apps.communication.models import Notification
    
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    return {'success': True}


# Announcements
@comm_router.get('/announcements/', response=list[AnnouncementSchema])
def list_announcements(request, audience: str = None):
    """Get announcements"""
    from apps.communication.models import Announcement
    from django.utils import timezone
    
    query = Announcement.objects.filter(expires_at__gt=timezone.now())
    if audience:
        query = query.filter(target_audience=audience)
    
    return query.order_by('-created_at')[:20]


@comm_router.get('/announcements/{announcement_id}')
def get_announcement(request, announcement_id: str):
    """Get single announcement"""
    from apps.communication.models import Announcement
    
    return Announcement.objects.get(id=announcement_id)


# Send notification (staff only)
@comm_router.post('/send/')
def send_notification(request, user_id: str, title: str, message: str):
    """Send notification to user"""
    from apps.communication.models import Notification
    from apps.accounts.models import User
    
    user = User.objects.get(id=user_id)
    notification = Notification.objects.create(
        user=user,
        title=title,
        message=message
    )
    return notification


# Broadcast announcement (admin)
@comm_router.post('/announcements/broadcast/')
def broadcast_announcement(request, title: str, content: str, priority: str = 'normal', audience: str = 'all'):
    """Broadcast announcement"""
    from apps.communication.models import Announcement
    
    announcement = Announcement.objects.create(
        title=title,
        content=content,
        priority=priority,
        target_audience=audience
    )
    return announcement
