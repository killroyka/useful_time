from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm, PasswordResetForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView, \
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView


class UserLoginView(LoginView):
    form_class = AuthenticationForm
    template_name = 'users/login.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
        return redirect('/')


class UserLogoutView(LogoutView):
    pass


class UserSignUpView(CreateView):
    form_class = UserCreationForm
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
    form_class = PasswordResetForm
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
