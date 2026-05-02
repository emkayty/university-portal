"""JWT Authentication for DRF"""
import jwt
from rest_framework import authentication, exceptions
from django.contrib.auth import get_user_model
from apps.accounts.jwt_utils import JWTManager

User = get_user_model()


class JWTAuthentication(authentication.BaseAuthentication):
    """JWT Token Authentication for DRF."""
    
    keyword = 'Bearer'
    
    def authenticate(self, request):
        """Authenticate the request and return (user, token) tuple."""
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            return None
            
        # Parse: "Bearer <token>"
        auth_parts = auth_header.split()
        
        if len(auth_parts) != 2 or auth_parts[0] != self.keyword:
            return None
            
        token = auth_parts[1]
        
        try:
            payload = JWTManager.verify_token(token)
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Token has expired')
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed('Invalid token')
        
        user = self.get_user(payload)
        
        if user is None:
            raise exceptions.AuthenticationFailed('User not found')
            
        if not user.is_active:
            raise exceptions.AuthenticationFailed('User is inactive')
            
        return (user, token)
    
    def get_user(self, payload):
        """Get user from token payload."""
        user_id = payload.get('user_id')
        
        if not user_id:
            return None
            
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None
    
    def authenticate_header(self, request):
        """Return the authentication header keyword."""
        return self.keyword