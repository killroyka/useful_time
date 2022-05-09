from django.forms import ValidationError
from re import match


def validate_color(value):
    if not match('^#([A-Fa-f0-9]{6})$', value):
        raise ValidationError('Цвет указан в неверном формате')
