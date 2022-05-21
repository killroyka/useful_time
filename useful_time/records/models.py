from datetime import datetime
from datetime import timedelta

from dateutil.tz import tzlocal
from django.db import models
from projects.models import Project


class Record(models.Model):
    project = models.ForeignKey(Project, verbose_name='Проект', related_name="records", on_delete=models.CASCADE)
    name = models.CharField('Название', help_text='не более 100 символов', max_length=100)
    avg_longitude = models.IntegerField("Продолжительность", default=0)
    startpoint = models.DateTimeField("Начало", blank=True, default=None, null=False)
    endpoint = models.DateTimeField("Конец", blank=True, default=None, null=True)

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'

    def __str__(self):
        return self.name

    def get_clean_back_longitude(self, sub_records):
        """Метод для бэка. Возвращает чистое время, потраченное на задание в секундах."""
        deltas = timedelta()
        for sub_record in sub_records:
            if sub_record.endpoint is None:
                deltas += datetime.now(tzlocal()) - sub_record.startpoint
            else:
                deltas += sub_record.endpoint - sub_record.startpoint
        return deltas.seconds + (deltas.days * 24 * 60 * 60)

    def get_clean_front_longitude(self, time) -> str:
        out = []
        seconds = time % 60
        minutes = time // 60 % 60
        hours = time // 60 // 60 % 24
        days = time // 60 // 60 // 24
        if days:
            out.append(f'{days} дн')
        if hours:
            out.append(f'{hours} ч')
        if minutes:
            out.append(f'{minutes} мин')
        if seconds:
            out.append(f'{seconds} сек')
        return ' '.join(out)

    def get_front_startpoint_and_endpoint(self, startpoint, endpoint) -> tuple:
        if startpoint is None:
            startpoint = 'Ещё не начался'
        if endpoint is None:
            endpoint = 'Ещё идёт'
        return startpoint, endpoint

    def set_subrecords(self):
        self.sub_records = self.subrecords.all()

    def get_startpoint_and_endpoint(self, sub_records) -> tuple:
        sub_records = list(sub_records)
        if sub_records[0].startpoint:
            startpoint = sub_records[0].startpoint
        else:
            startpoint = None
        if sub_records[-1].endpoint:
            endpoint = sub_records[-1].startpoint
        else:
            endpoint = None
        return startpoint, endpoint

    def get_data(self):
        sub_records = self.subrecords.all()
        clean_back_longitude = self.get_clean_back_longitude(sub_records)
        clean_front_longitude = self.get_clean_front_longitude(clean_back_longitude)
        startpoint_and_endpoint = self.get_startpoint_and_endpoint(sub_records)
        front_startpoint_and_endpoint = self.get_front_startpoint_and_endpoint(startpoint_and_endpoint[0],
                                                                               startpoint_and_endpoint[1])
        return {"clean_front_longitude": clean_front_longitude,
                "clean_back_longitude": clean_back_longitude,
                "startpoint_and_endpoint": startpoint_and_endpoint,
                "front_startpoint_and_endpoint": front_startpoint_and_endpoint}


class SubRecord(models.Model):
    record = models.ForeignKey(Record, verbose_name='Таймер', related_name='subrecords', on_delete=models.CASCADE)
    startpoint = models.DateTimeField('Начало', blank=False, null=False)
    endpoint = models.DateTimeField('Конец', blank=True, null=True)

    class Meta:
        verbose_name = 'Подзапись'
        verbose_name_plural = 'Подзаписи'

    def __str__(self):
        return f"{self.record}(start:{bool(self.startpoint)}, stop:{bool(self.endpoint)})"

    @property
    def get_back_longitude(self) -> int:
        """Метод для бэка. Возвращает время, потраченное на задание в секундах.
         Если запись ещё не завершена, то вернет -1"""
        if self.endpoint is None:
            return -1
        print(type(self.endpoint), type(self.startpoint))
        time = self.endpoint - self.startpoint
        return time.seconds + (time.days * 24 * 60 * 60)

    @property
    def get_front_longitude(self) -> str:
        """Метод для фронта. Возвращает время, потраченное на задание в человекочитаемом формате.
         Если запись ещё не завершена, то вернет строку 'Ещё идет' """
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
