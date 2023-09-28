from datetime import datetime

from django.core.exceptions import ValidationError


def validate_year(value):
    if isinstance(value, dict):
        validate_value = value.get('year')
    else:
        validate_value = value

    if validate_value and validate_value > datetime.now().year:
        raise ValidationError(
            'Указанный год выпуска произведения еще не наступил.'
        )
    return value
