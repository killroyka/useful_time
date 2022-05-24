from django.contrib.auth.forms import (AuthenticationForm, PasswordChangeForm)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (LoginView, LogoutView,
                                       PasswordChangeDoneView,
                                       PasswordChangeView,
                                       PasswordResetCompleteView,
                                       PasswordResetConfirmView,
                                       PasswordResetDoneView,
                                       PasswordResetView)
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView
from django_currentuser.middleware import (
    get_current_user)
from projects.models import Project
from users.forms import RegistrationForm, EmailValidationResetPasswordForm, UserEditForm
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


class Profile(LoginRequiredMixin, FormView):
    model = User
    template_name = 'users/profile.html'
    form_class = UserEditForm
    success_url = reverse_lazy('profile')

    def get_context_data(self, **kwargs):
        user = get_current_user()
        form = UserEditForm(initial={"username": user.username, "email": user.email})
        projects = Project.objects.filter(user__id=user.id)
        return {"projects": projects, "form": form}

    def post(self, request, *args, **kwargs):
        form = Profile.form_class(request.POST)
        if form.is_valid():
            form.save()
        return redirect(reverse_lazy('profile'))
