from colorfield.fields import ColorField
from django.db import models
from .validators import validate_color
from users.models import User
from django.apps import apps



class Project(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь', related_name="projects", on_delete=models.CASCADE)
    name = models.CharField('Название', help_text='не более 20 символов', max_length=20)
    description = models.TextField('Описание', help_text='не более 200 символов', max_length=200)
    color = ColorField('Цвет', format='hex', validators=[validate_color])

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'


    def __str__(self):
        return self.name

    def get_diogramm_data(self):
        records = apps.get_model('records.Record').objects.filter(project__id=self.id)
        diogramm_data_names = []
        diogramm_data = []
        for record in records:
            if record.get_back_longitude() != -1:
                diogramm_data_names.append(record.name)
                diogramm_data.append(record.get_back_longitude())
        return {"diogramm_data_names": diogramm_data_names, "diogramm_data": diogramm_data}
