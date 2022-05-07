from django.urls import path

from . import views
from .views import HomePage

urlpatterns = [
    path("", HomePage.as_view(), name="homepage")
]