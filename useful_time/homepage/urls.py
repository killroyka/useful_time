from django.urls import path
from .views import HomePage
from . import views


urlpatterns = [
    path("", HomePage.as_view(), name="homepage")
]