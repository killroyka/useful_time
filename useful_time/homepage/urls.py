from django.urls import path

from .views import HomePage, FAQs

urlpatterns = [
    path("", HomePage.as_view(), name="homepage"),
    path("FAQs/", FAQs.as_view(), name="FAQs")
]
