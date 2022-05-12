from django.core.validators import ValidationError
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

    def clean(self):
        if self.endpoint is not None:
            if self.startpoint >= self.endpoint:
                raise ValidationError('Обратите внимание на дату и время: нельзя закончить то, что ещё не началось')

    def get_startpoint_isoformat(self) -> str:
        return self.startpoint.isoformat()

    @property
    def get_back_longitude(self) -> int:
        """Метод для бэка. Возвращает время, потраченное на задание в секундах.
         Если запись ещё не завершена, то вернет -1"""
        if self.endpoint is None:
            return -1
        time = self.endpoint - self.startpoint
        return time.seconds + (time.days * 24 * 60 * 60)

    @property
    def get_front_longitude(self) -> str:
        """Метод для фронта. Возвращает время, потраченное на задание в человекочитаемом формате.
         Если запись ещё не завершена, то вернет строку 'Ещё идет' """
        if self.endpoint is None:
            return 'Ещё идет'
        out = []
        datetime = (self.endpoint - self.startpoint)
        time = datetime.seconds
        seconds = time % 60
        minutes = time // 60 % 60
        hours = time // 60 // 60 % 24
        days = datetime.days
        if days:
            out.append(f'{days} дн')
        if hours:
            out.append(f'{hours} ч')
        if minutes:
            out.append(f'{minutes} мин')
        if seconds:
            out.append(f'{seconds} сек')
        return ' '.join(out)
