from datetime import datetime

from django.forms import ModelForm, TextInput, DateInput

from .models import Record


class RecordForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(RecordForm, self).__init__(*args, **kwargs)
        self.initial['startpoint'] = self.initial['startpoint'].replace(microsecond=0, tzinfo=None).isoformat()
        self.initial['endpoint'] = self.initial['endpoint'].replace(microsecond=0, tzinfo=None).isoformat()


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


class NewRecordForm(RecordForm):
    class Meta(RecordForm.Meta):
        fields = ('name', 'project', 'startpoint')
        widgets = {
            'startpoint': DateInput(
                attrs={
                    'type': 'datetime-local',
                    'step': '1',
                    'value': datetime.now().replace(microsecond=0).isoformat()
                },
            ),
        }