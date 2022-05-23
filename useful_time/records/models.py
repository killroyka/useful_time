from django.db import models
from projects.models import Project


class Record(models.Model):
    project = models.ForeignKey(
        Project,
        verbose_name='Проект',
        related_name="records",
        on_delete=models.CASCADE
    )

    name = models.CharField(
        'Название',
        help_text='не более 100 символов',
        max_length=100
    )

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'

    def __str__(self):
        return self.name


class SubRecord(models.Model):
    record = models.ForeignKey(
        Record,
        verbose_name='Таймер',
        related_name='subrecords',
        on_delete=models.CASCADE
    )

    startpoint = models.DateTimeField(
        'Начало',
        blank=False,
        null=False
    )

    endpoint = models.DateTimeField(
        'Конец',
        blank=True,
        null=True
    )

    longitude = models.IntegerField(
        'продолжительность',
        blank=True,
        null=True,
        default=0
    )

    class Meta:
        verbose_name = 'Подзапись'
        verbose_name_plural = 'Подзаписи'
        ordering = ['-endpoint']

    def __str__(self):
        return f'{self.record}(start:{bool(self.startpoint)},' \
               f' stop:{bool(self.endpoint)})'

    @property
    def get_back_longitude(self) -> int:
        """Метод для бэка. Возвращает время, потраченное на задание в секундах.
         Если запись ещё не завершена, то вернет -1"""
        if self.endpoint is None:
            return -1
        time = self.endpoint - self.startpoint.replace(tzinfo=None)
        return time.seconds + (time.days * 24 * 60 * 60)

    @property
    def get_front_longitude(self) -> str:
        """Метод для фронта. Возвращает время, потраченное на
         задание в человекочитаемом формате. Если запись ещё не
          завершена, то вернет строку 'Ещё идет' """
        if self.endpoint is None:
            return 'Ещё идет'
        out = []
        dt = (self.endpoint - self.startpoint)
        time = dt.seconds
        seconds = time % 60
        minutes = time // 60 % 60
        hours = time // 60 // 60 % 24
        days = dt.days
        if days:
            out.append(f'{days} дн')
        if hours:
            out.append(f'{hours} ч')
        if minutes:
            out.append(f'{minutes} мин')
        if seconds:
            out.append(f'{seconds} сек')
        return ' '.join(out)
