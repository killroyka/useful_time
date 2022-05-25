from django.urls import path

from . import views

urlpatterns = [
    # Регистрация
    path('signup/', views.UserSignUpView.as_view(),
         name='signup'),
    path('login/', views.UserLoginView.as_view(),
         name='login'),
    path('logout/', views.UserLogoutView.as_view(),
         name='logout'),
    path('password_change/', views.UserPasswordChangeView.as_view(),
         name='password_change'),
    path('password_change/done/', views.UserPasswordChangeDoneView.as_view(),
         name='password_change_done'),
    path('password_reset/', views.UserPasswordResetView.as_view(),
         name='password_reset'),
    path('password_reset/done/', views.UserPasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/',
         views.UserPasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('password_reset_complete/',
         views.UserPasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
    # /Регистрация

    path('profile/<int:pk>', views.Profile.as_view(), name='profile')

]
