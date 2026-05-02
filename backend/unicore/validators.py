"""Validators - Nigerian University Standards"""
import re
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

# === NIGERIAN PHONE NUMBER ===
def validate_nigerian_phone(value):
    """Validate Nigerian phone number (0801, 0802, etc.)"""
    pattern = r'^(?:\+?234|0)?(?:81[0-2]|80[2-9]|70[0-9]|90[1-9])\d{8}$'
    if not re.match(pattern, str(value)):
        raise ValidationError(
            'Enter a valid Nigerian phone number (e.g., 08031234567)'
        )

# === NIGERIAN NIN (11 digits) ===
def validate_nin(value):
    """Validate Nigerian National ID Number (11 digits)"""
    if not re.match(r'^\d{11}$', str(value)):
        raise ValidationError(
            'NIN must be exactly 11 digits'
        )

# === MATRIC NUMBER ===
def validate_matric_number(value):
    """Validate Nigerian matric number format"""
    # Example: UNI/2020/001234
    pattern = r'^[A-Z]{2,10}/\d{4}/\d{6}$'
    if not re.match(pattern, str(value)):
        raise ValidationError(
            'Enter a valid matric number (e.g., UNN/2020/123456)'
        )

# === NIGERIAN BANK ACCOUNT ===
def validate_account_number(value):
    """Validate Nigerian bank account (10 digits)"""
    if not re.match(r'^\d{10}$', str(value)):
        raise ValidationError(
            'Account number must be exactly 10 digits'
        )

# === JAMB REG NUMBER ===
def validate_jamb_reg(value):
    """Validate JAMB registration number"""
    pattern = r'^\d{10}$|^\d{12}$'
    if not re.match(pattern, str(value)):
        raise ValidationError(
            'Enter a valid JAMB registration number'
        )

# === BLOOD TYPE ===
def validate_blood_type(value):
    valid = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
    if value and value.upper() not in valid:
        raise ValidationError(
            f'Blood type must be one of: {", ".join(valid)}'
        )

# === STUDENT LEVEL ===
def validate_level(value):
    """Validate student level (100-600)"""
    valid_levels = [100, 200, 300, 400, 500, 600]
    if value and value not in valid_levels:
        raise ValidationError(
            f'Level must be one of: {", ".join(map(str, valid_levels))}'
        )
