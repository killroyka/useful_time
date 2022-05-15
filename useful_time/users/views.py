from django.contrib.auth.forms import (AuthenticationForm, PasswordChangeForm,
                                       PasswordResetForm, UserCreationForm)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (LoginView, LogoutView,
                                       PasswordChangeDoneView,
                                       PasswordChangeView,
                                       PasswordResetCompleteView,
                                       PasswordResetConfirmView,
                                       PasswordResetDoneView,
                                       PasswordResetView)
from django.core.mail import EmailMessage
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView
from django.views.generic.base import TemplateView
from django_currentuser.middleware import (
    get_current_user, get_current_authenticated_user)
from projects.models import Project

from users.forms import RegistrationForm, EmailValidationResetPasswordForm
from users.models import User


class UserLoginView(LoginView):
    form_class = AuthenticationForm
    template_name = 'users/login.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
        return redirect('/')


class UserLogoutView(LogoutView):
    success_url = '/'


class UserSignUpView(CreateView):
    form_class = RegistrationForm
    success_url = reverse_lazy('login')
    template_name = 'users/signup.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
        return redirect('/')

    # def post(self, request, *args, **kwargs):
    #     self.object = None
    #     form_user = UserSignUpView.form_class(request.POST or None)
    #     if form_user.is_valid():
    #         message = EmailMessage('Подтверждение', 'Пароль 000000', to=[form_user.cleaned_data['email']])
    #         message.send()
    #         return self.form_valid(form_user)
    #     return self.form_invalid(form_user)


class UserPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('password_change_done')
    template_name = 'users/password_change.html'


class UserPasswordChangeDoneView(LoginRequiredMixin, PasswordChangeDoneView):
    success_url = '/'
    template_name = 'users/password_change_done.html'


class UserPasswordResetView(PasswordResetView):
    form_class = EmailValidationResetPasswordForm
    success_url = reverse_lazy('password_reset_done')
    template_name = 'users/password_reset.html'


class UserPasswordResetDoneView(PasswordResetDoneView):
    success_url = '/'
    template_name = 'users/password_reset_done.html'


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    success_url = reverse_lazy('password_reset_complete')
    template_name = 'users/password_reset_confirm.html'


class UserPasswordResetCompleteView(PasswordResetCompleteView):
    success_url = '/'
    template_name = 'users/password_reset_complete.html'


class Profile(LoginRequiredMixin, TemplateView):
    template_name = 'users/profile.html'

    def get_context_data(self, **kwargs):
        user = get_current_user()
        projects = Project.objects.filter(user__id=user.id)
        diogramm_data_names = ["WordPress", "Joomla", "Drupal", "Blogger", "Magento"]
        diogramm_data = [60.7, 7.4, 5.1, 2.9, 2.8]
        return {"projects": projects, "diogramm_data_names": diogramm_data_names, "diogramm_data": diogramm_data}
