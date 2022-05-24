from django.forms import ValidationError
from re import match


def validate_color(value):
    """
    Валидатор цвета (устаревший, т.к. на фронте используется
    специальна форма ввода цвета, которая сама не
    допустит невозможного ответа)
    """
    if not match('^#([A-Fa-f0-9]{6})$', value):
        raise ValidationError('Цвет указан в неверном формате')
