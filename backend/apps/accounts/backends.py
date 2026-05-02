"""
Custom Authentication Backend for UniCore

Supports email + password authentication with UUID primary keys.
"""
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model

User = get_user_model()


class EmailBackend(BaseBackend):
    """
    Authentication backend that supports email-based login.
    
    Works with UUID primary keys and custom User model.
    """
    
    def authenticate(self, request, email=None, password=None, **kwargs):
        if email is None or password is None:
            return None
            
        try:
            user = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            # Run password hashers to prevent timing attacks
            User().set_password(password)
            return None
            
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
    
    def user_can_authenticate(self, user):
        """Block non-active users."""
        is_active = getattr(user, 'is_active', None)
        return is_active or is_active is None
    
    def get_user(self, user_id):
        """Retrieve user by UUID."""
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
            
        if self.user_can_authenticate(user):
            return user
        return None


class UUIDBackend(BaseBackend):
    """
    Authentication backend that supports UUID-based login.
    Primarily for token refresh operations.
    """
    
    def authenticate(self, request, user_id=None, **kwargs):
        if user_id is None:
            return None
            
        try:
            user = User.objects.get(pk=user_id)
        except (User.DoesNotExist, ValueError):
            return None
            
        if self.user_can_authenticate(user):
            return user
        return None
    
    def user_can_authenticate(self, user):
        return getattr(user, 'is_active', True)
    
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except (User.DoesNotExist, ValueError):
            return None