import re
from django.core.exceptions import ValidationError


def validate_phone_number(value):
    pattern = r"^[6-9]\d{9}$"
    if not re.match(pattern, value):
        raise ValidationError(
            "Invalid Phone number format. Must be 10 digit number starting with 6-9"
        )
