"""Communication API - Announcements, Messages, Notifications"""
from ninja import Schema
from ninjaJWT import router as communication_router


class AnnouncementSchema(Schema):
    id: str
    title: str
    body: str
    scope: str
    posted_at: str


class NotificationSchema(Schema):
    id: str
    message: str
    is_read: bool
    created_at: str


# Announcements
@communication_router.get('/announcements', response=list[AnnouncementSchema])
def list_announcements(request, scope: str = None):
    """List announcements"""
    from apps.communication.models import Announcement
    query = Announcement.objects.all()
    if scope:
        query = query.filter(scope=scope)
    return query


@communication_router.post('/announcements')
def create_announcement(request, title: str, body: str, scope: str = 'global'):
    """Create announcement"""
    from apps.communication.models import Announcement
    
    announcement = Announcement.objects.create(
        title=title,
        body=body,
        scope=scope,
        posted_by=request.user
    )
    return announcement


# Notifications
@communication_router.get('/notifications', response=list[NotificationSchema])
def list_notifications(request):
    """List user notifications"""
    from apps.communication.models import Notification
    return Notification.objects.filter(user=request.user)


@communication_router.post('/notifications/{notification_id}/read')
def mark_notification_read(request, notification_id: str):
    """Mark notification as read"""
    from apps.communication.models import Notification
    
    notification = Notification.objects.get(id=notification_id)
    notification.is_read = True
    notification.save()
    return notification