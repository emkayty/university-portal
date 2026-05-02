"""Accounts API - Authentication & User Management"""
from datetime import datetime
from ninja import Schema, Field
from typing import Optional
from ninjaJWT import router as accounts_router


class UserSchema(Schema):
    id: str
    email: str
    role: str
    first_name: Optional[str]
    last_name: Optional[str]
    is_active: bool


class LoginSchema(Schema):
    email: str
    password: str


class TokenSchema(Schema):
    access: str
    refresh: Optional[str]


class RefreshSchema(Schema):
    refresh: str


@accounts_router.post('/login', response=TokenSchema)
def login(request, data: LoginSchema):
    from django.contrib.auth import authenticate
    from apps.accounts.models import User
    from ninjaJWT.token import create_access_token, create_refresh_token
    
    user = authenticate(username=data.email, password=data.password)
    if not user:
        return 401, {'error': 'Invalid credentials'}
    
    # Update last login
    user.last_login = datetime.now()
    user.save(update_fields=['last_login'])
    
    # Create tokens
    access_token = create_access_token({'user_id': str(user.id)})
    refresh_token = create_refresh_token({'user_id': str(user.id)})
    
    return {
        'access': access_token,
        'refresh': refresh_token
    }


@accounts_router.post('/refresh', response=TokenSchema)
def refresh(request, data: RefreshSchema):
    from ninjaJWT.token import decode_token, create_access_token, create_refresh_token
    
    try:
        token_data = decode_token(data.refresh)
        user_id = token_data.get('user_id')
        
        access_token = create_access_token({'user_id': user_id})
        refresh_token = create_refresh_token({'user_id': user_id})
        
        return {
            'access': access_token,
            'refresh': refresh_token
        }
    except Exception as e:
        return 401, {'error': str(e)}


@accounts_router.get('/me', response=UserSchema)
def me(request):
    from apps.accounts.models import User
    
    if not request.user.is_authenticated:
        return 401, None
    
    return request.user


@accounts_router.get('/logout')
def logout(request):
    # JWT tokens are stateless - client handles token removal
    return {'message': 'Logged out successfully'}