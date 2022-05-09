from django.forms import ModelForm, TextInput

from .models import Record


class NewRecordForm(ModelForm):
    class Meta:
        model = Record
        fields = ('name', 'project', 'startpoint')
        widgets = {
            'startpoint': TextInput(attrs={'type': 'datetime-local', 'step': '1'}),
        }
