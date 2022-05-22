from django.forms import BooleanField
from django.forms import ModelForm, DateInput

from .models import Record


class RecordForm(ModelForm):
    def __init__(self, user=None, *args, **kwargs):
        """Переопределение метода __init__ для того, чтобы изменить queryset
         проектов - отфильтровать их по совпадению user_id"""
        super(RecordForm, self).__init__(*args, **kwargs)
        if user is not None:
            self.initial['project'].queryset = \
                self.initial['project'].queryset.filter(user_id=user.id)

    class Meta:
        model = Record
        fields = ('name', 'project')
        widgets = {
            'startpoint': DateInput(
                attrs={
                    'type': 'datetime-local',
                    'step': '1',
                },
            ),
            'endpoint': DateInput(
                attrs={
                    'type': 'datetime-local',
                    'step': '1'
                }
            )
        }


class NewRecordForm(ModelForm):
    start_right_now = BooleanField(
        required=False,
        label='Начать запись сразу после отправки формы'
    )

    class Meta(RecordForm.Meta):
        fields = ('name', 'project')
        widgets = {
            'startpoint': DateInput(
                attrs={
                    'type': 'datetime-local',
                    'step': '1'
                },
            )
        }
