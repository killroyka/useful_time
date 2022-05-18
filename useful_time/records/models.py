from django.db import models

from projects.models import Project


class Record(models.Model):
    project = models.ForeignKey(Project, verbose_name='Проект', related_name="records", on_delete=models.CASCADE)
    name = models.CharField('Название', help_text='не более 100 символов', max_length=100)

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'

    def __str__(self):
        return self.name

    @property
    def get_back_longitude(self) -> int:
        """Метод для бэка. Возвращает время, потраченное на задание в секундах.
         Если запись ещё не завершена, то вернет -1"""
        startpoint, endpoint = self.get_startpoint_and_endpoint()
        if endpoint is None:
            return -1
        time = endpoint - startpoint
        return time.seconds + (time.days * 24 * 60 * 60)

    @property
    def get_front_longitude(self) -> str:
        """Метод для фронта. Возвращает время, потраченное на задание в человекочитаемом формате.
         Если запись ещё не завершена, то вернет строку 'Ещё идет' """
        startpoint, endpoint = self.get_startpoint_and_endpoint()
        if endpoint is None:
            return 'Ещё идет'
        out = []
        datetime = (endpoint - startpoint)
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

    def get_front_startpoint_and_endpoint(self):
        startpoint, endpoint = self.get_startpoint_and_endpoint()
        if startpoint is None:
            startpoint = 'Ещё не начался'
        if endpoint is None:
            endpoint = 'Ещё идёт'
        return startpoint, endpoint

    def set_subrecords(self):
        self.sub_records = self.subrecords.all()

    def get_startpoint_and_endpoint(self):
        startpoints = [i.startpoint for i in self.sub_records]
        if startpoints:
            startpoint = min(startpoints)
        else:
            startpoint = None

        endpoints = [i.endpoint for i in self.sub_records]
        if all(endpoints):
            endpoint = max(endpoints)
        else:
            endpoint = None

        return startpoint, endpoint


class SubRecord(models.Model):
    record = models.ForeignKey(Record, verbose_name='Таймер', related_name='subrecords', on_delete=models.CASCADE)
    startpoint = models.DateTimeField('Начало', blank=False, null=False)
    endpoint = models.DateTimeField('Конец', blank=True, null=True)

    class Meta:
        verbose_name = 'Подзапись'
        verbose_name_plural = 'Подзаписи'

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
