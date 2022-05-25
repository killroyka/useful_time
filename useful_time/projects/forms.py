from re import match

from django.forms import ModelForm
from django.forms import ValidationError

from .models import Project


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ("name", "description", "color")


    def clean_color(self):
        """
        Валидатор цвета (устаревший, т.к. на фронте используется
        специальна форма ввода цвета, которая сама не
        допустит невозможного ответа)
        """
        data = self.cleaned_data['color']
        if not match('^#([A-Fa-f0-9]{6})$', data):
            raise ValidationError(
                'Цвет указан в неверном формате',
                code='invalid'
            )

        return data
