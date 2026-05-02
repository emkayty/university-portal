"""JWT Authentication Utilities for UniCore"""
import jwt
from datetime import datetime, timedelta
from typing import Optional
from django.conf import settings


class JWTManager:
    """JWT Token Manager with secure defaults."""
    
    ALGORITHM = 'HS256'
    TOKEN_TYPE = 'access'
    REFRESH_TYPE = 'refresh'
    
    # Token lifetimes
    ACCESS_TOKEN_LIFETIME = timedelta(minutes=60)  # 1 hour
    REFRESH_TOKEN_LIFETIME = timedelta(days=7)  # 7 days
    
    @classmethod
    def get_secret_key(cls, token_type: str = 'access') -> str:
        """Get signing key - prefer dedicated JWT key."""
        if token_type == 'refresh':
            key = getattr(settings, 'JWT_REFRESH_SECRET_KEY', None)
            return key or settings.SECRET_KEY
        return getattr(settings, 'JWT_ACCESS_SECRET_KEY', None) or settings.SECRET_KEY
    
    @classmethod
    def create_token(cls, user_id: str, email: str, role: str, token_type: str = 'access') -> str:
        """Create a JWT token for a user."""
        if token_type == 'access':
            lifetime = cls.ACCESS_TOKEN_LIFETIME
        else:
            lifetime = cls.REFRESH_TOKEN_LIFETIME
        
        payload = {
            'user_id': str(user_id),
            'email': email,
            'role': role,
            'type': token_type,
            'exp': datetime.utcnow() + lifetime,
            'iat': datetime.utcnow(),
        }
        
        secret = cls.get_secret_key(token_type)
        token = jwt.encode(payload, secret, algorithm=cls.ALGORITHM)
        return token
    
    @classmethod
    def create_access_token(cls, user) -> str:
        """Create access token for user."""
        return cls.create_token(
            user_id=str(user.id),
            email=user.email,
            role=user.role,
            token_type=cls.TOKEN_TYPE
        )
    
    @classmethod
    def create_refresh_token(cls, user) -> str:
        """Create refresh token for user."""
        return cls.create_token(
            user_id=str(user.id),
            email=user.email,
            role=user.role,
            token_type=cls.REFRESH_TYPE
        )
    
    @classmethod
    def decode_token(cls, token: str, token_type: str = 'access') -> dict:
        """Decode and validate a JWT token."""
        try:
            secret = cls.get_secret_key(token_type)
            payload = jwt.decode(token, secret, algorithms=[cls.ALGORITHM])
            
            # Validate token type
            if payload.get('type') != token_type:
                raise jwt.InvalidTokenError(f"Expected {token_type} token")
                
            return payload
        except jwt.ExpiredSignatureError:
            raise jwt.InvalidTokenError("Token has expired")
        except jwt.InvalidTokenError:
            raise
    
    @classmethod
    def verify_token(cls, token: str) -> dict:
        """Verify access token and return payload."""
        return cls.decode_token(token, cls.TOKEN_TYPE)
    
    @classmethod
    def verify_refresh_token(cls, token: str) -> dict:
        """Verify refresh token and return payload."""
        return cls.decode_token(token, cls.REFRESH_TYPE)
    
    @classmethod
    def refresh_access_token(cls, refresh_token: str) -> str:
        """Generate new access token from refresh token."""
        payload = cls.verify_refresh_token(refresh_token)
        
        # Create new access token
        from apps.accounts.models import User
        try:
            user = User.objects.get(id=payload['user_id'])
        except User.DoesNotExist:
            raise jwt.InvalidTokenError("User not found")
        
        return cls.create_access_token(user)


def create_tokens_for_user(user) -> dict:
    """Helper to create both access and refresh tokens."""
    return {
        'access': JWTManager.create_access_token(user),
        'refresh': JWTManager.create_refresh_token(user),
        'expires_in': int(JWTManager.ACCESS_TOKEN_LIFETIME.total_seconds())
    }


def verify_and_get_user(token: str):
    """Verify token and return the user."""
    from apps.accounts.models import User
    
    try:
        payload = JWTManager.verify_token(token)
        return User.objects.get(id=payload['user_id'])
    except (jwt.InvalidTokenError, User.DoesNotExist):
        return None