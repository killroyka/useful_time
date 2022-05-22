from django.contrib import admin
from django import forms

from users.models import User
from users.forms import RegistrationForm


class UserAdminForm(RegistrationForm, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True

    class Meta:
        model = User
        exclude = ('password',)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    form = UserAdminForm
