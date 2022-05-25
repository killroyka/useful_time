from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import PasswordResetForm, AuthenticationForm
from django.core.exceptions import ValidationError

from users.models import User


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email')


class RegistrationForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.PasswordInput
    )


    class Meta:
        model = User
        fields = ('username', 'email')


    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Пароли не совпали')
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class EmailValidationResetPasswordForm(PasswordResetForm):
    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email__iexact=email, is_active=True).exists():
            raise ValidationError("Введён некорректный почтовый адрес!")

        return email


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'email')


    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).first() is None:
            raise forms.ValidationError(
                "Такого пользователя нет. Учтите, что поля чувствительны к регистру.")
        else:
            return username

    def clean_password(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username is not None and password:
            user_cache = authenticate(self.request, username=username, password=password)
            if user_cache is None:
                raise forms.ValidationError(
                    "Неверный пароль. Учтите, что поля чувствительны к регистру.")
        return password
