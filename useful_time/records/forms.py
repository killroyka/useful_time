from datetime import datetime

from dateutil.tz import tzlocal
from django.forms import BooleanField
from django.forms import ModelForm, DateInput

from useful_time.settings import DATE_INPUT_FORMATS
from .models import Record


class RecordForm(ModelForm):
    def __init__(self, user=None, *args, **kwargs):
        super(RecordForm, self).__init__(*args, **kwargs)
        self.initial['startpoint'] = self.initial['startpoint'].strftime(DATE_INPUT_FORMATS[0])
        self.initial['endpoint'] = self.initial['endpoint'].strftime(DATE_INPUT_FORMATS[0])
        if user is not None:
            self.initial['project'].queryset = self.initial['project'].queryset.filter(user_id=user.id)

    class Meta:
        model = Record
        fields = ('name', 'project', 'startpoint', 'endpoint')
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
    start_right_now = BooleanField(required=False, label='Начать запись сразу после отправки формы')

    class Meta(RecordForm.Meta):
        fields = ('name', 'project', 'startpoint')
        widgets = {
            'startpoint': DateInput(
                attrs={
                    'type': 'datetime-local',
                    'step': '1',
                    'value': datetime.now(tzlocal()).strftime(DATE_INPUT_FORMATS[0])
                },
            )
        }
