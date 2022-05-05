from django.db import models
from projects.models import Project


class Record(models.Model):
    project = models.ForeignKey(Project, verbose_name='Проект', related_name="records", default='Безымянный промежуток',
                                on_delete=models.CASCADE)
    name = models.CharField('Название', help_text='не более 100 символов', max_length=100)
    startpoint = models.DateTimeField('Начало', blank=False, null=False)
    endpoint = models.DateTimeField('Конец', blank=True, null=True)


    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'


    def __str__(self):
        return self.name

    def get_back_longitude(self):
        pass

    def get_front_longitude(self):
        pass




