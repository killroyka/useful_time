from datetime import datetime

from django.forms import ModelForm, TextInput, DateInput

from .models import Record


class RecordForm(ModelForm):
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
