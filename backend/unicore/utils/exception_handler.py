"""
UniCore Exception Handler

Standardizes error responses across the application.
"""
import logging
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """Handle exceptions with consistent JSON responses."""
    response = exception_handler(exc, context)
    
    if response is not None:
        # Standardize DRF error format
        error_data = {
            'success': False,
            'status_code': response.status_code,
            'error': transform_error_data(response.data),
        }
        response.data = error_data
        response.content_type = 'application/json'
    
    return response


def transform_error_data(data):
    """Transform DRF error format to simpler format."""
    if isinstance(data, dict):
        # Field errors
        errors = []
        for field, messages in data.items():
            field_name = field.replace('_', ' ').title()
            if isinstance(messages, list):
                for msg in messages:
                    errors.append(f"{field_name}: {msg}")
            else:
                errors.append(f"{field_name}: {messages}")
        return errors if errors else [str(data)]
    elif isinstance(data, list):
        return [str(item) for item in data]
    return [str(data)]


class APIException(Exception):
    """Base API Exception with standard format."""
    
    status_code = status.HTTP_400_BAD_REQUEST
    default_message = 'An error occurred'
    error_code = 'error'
    
    def __init__(self, message=None, status_code=None, error_code=None):
        self.message = message or self.default_message
        if status_code:
            self.status_code = status_code
        if error_code:
            self.error_code = error_code
        super().__init__(self.message)
    
    def to_response(self):
        return Response(
            {
                'success': False,
                'error': self.message,
                'error_code': self.error_code,
            },
            status=self.status_code
        )


class NotFoundError(APIException):
    """Resource not found."""
    status_code = status.HTTP_404_NOT_FOUND
    default_message = 'Resource not found'
    error_code = 'not_found'


class ValidationError(APIException):
    """Validation error."""
    status_code = status.HTTP_400_BAD_REQUEST
    default_message = 'Invalid data'
    error_code = 'validation_error'


class AuthenticationError(APIException):
    """Authentication error."""
    status_code = status.HTTP_401_UNAUTHORIZED
    default_message = 'Authentication required'
    error_code = 'authentication_error'


class PermissionError(APIException):
    """Permission denied."""
    status_code = status.HTTP_403_FORBIDDEN
    default_message = 'Permission denied'
    error_code = 'permission_denied'


def api_response(data=None, message=None, success=True, status_code=200):
    """Standard API response helper."""
    response_data = {
        'success': success,
    }
    if data is not None:
        response_data['data'] = data
    if message:
        response_data['message'] = message
    
    return Response(response_data, status=status_code)


def api_error(message, error_code=None, status_code=400):
    """Standard error response helper."""
    return api_response(
        data=None,
        message=message,
        success=False,
        status_code=status_code
    )