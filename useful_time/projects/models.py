from colorfield.fields import ColorField
from django.apps import apps
from django.db import models
from django.db.models import Sum
from users.models import User

from .validators import validate_color


class Project(models.Model):
    """
    Проектом мы называем объект содержащий в себе
    записи или таймеры, привязан к ОДНОМУ пользователю.
    """

    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        related_name="projects",
        on_delete=models.CASCADE
    )

    name = models.CharField(
        'Название',
        help_text='не более 20 символов',
        max_length=20
    )

    description = models.TextField(
        'Описание',
        help_text='не более 200 символов',
        max_length=200
    )

    color = ColorField(
        'Цвет',
        format='hex',
        validators=[validate_color]
    )


    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'


    def __str__(self):
        return self.name

    def get_diogramm_data(self):
        """
        Метод для фронта. Возвращает данные для
        отрисовки диограмм.
        """
        records = apps.get_model(
            'records.Record'
        ).objects.filter(
            project__id=self.id
        ).prefetch_related(
            "subrecords"
        ).annotate(
            longitude=Sum("subrecords__longitude")
        )

        diogramm_data_names = []
        diogramm_data = []
        for record in records:
            diogramm_data_names.append(record.name)
            diogramm_data.append(record.longitude)

        return {"diogramm_data_names": diogramm_data_names,
                "diogramm_data": diogramm_data}
