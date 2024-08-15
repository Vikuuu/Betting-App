from django.core.exceptions import ValidationError


def pick_validation(value):
    if value < 1 and value > 36:
        raise ValidationError("Pick Number must be between 1 to 36")
