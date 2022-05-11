from django.forms import ModelForm
from colorfield.fields import ColorField
from django.forms import ValidationError
from .models import Project
from re import match


class NewProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ("name", "description", "color")

    def clean_color(self):
        data = self.cleaned_data['color']
        if not match('^#([A-Fa-f0-9]{6})$', data):
            raise ValidationError('Цвет указан в неверном формате', code='invalid')

        return data
