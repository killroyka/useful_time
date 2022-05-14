from datetime import datetime

from django.forms import ModelForm, DateInput, BooleanField, CheckboxInput
from django.forms import ModelForm, DateInput
from django.utils.timezone import utc

from useful_time.settings import DATE_INPUT_FORMATS
from .models import Record


class RecordForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(RecordForm, self).__init__(*args, **kwargs)
        self.initial['startpoint'] = self.initial['startpoint'].strftime(DATE_INPUT_FORMATS[0])
        self.initial['endpoint'] = self.initial['endpoint'].strftime(DATE_INPUT_FORMATS[0])

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
                    'value': datetime.now().replace(tzinfo=utc).strftime(DATE_INPUT_FORMATS[0])
                },
            )
        }
