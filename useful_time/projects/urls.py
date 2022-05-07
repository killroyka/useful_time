from django.urls import path

from . import views
from .views import ProjectsListView

urlpatterns = [
    path("", ProjectsListView.as_view(), name="projects_list_view")
]