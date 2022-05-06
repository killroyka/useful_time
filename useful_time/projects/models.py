from django.db import models
from colorfield.fields import ColorField
from users.models import User


class Project(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь', related_name="projects", on_delete=models.CASCADE)
    name = models.CharField('Название', help_text='не более 100 символов', max_length=100)
    description = models.TextField('Описание', help_text='не более 500 символов', max_length=500)
    color = ColorField('Цвет', format='hex')

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'

    def __str__(self):
        return self.name

