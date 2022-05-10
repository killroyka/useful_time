from django.urls import path
from .views import ProjectsListView, ProjectAddView

urlpatterns = [
    path("", ProjectsListView.as_view(), name="projects_list_view"),
    path("add/", ProjectAddView.as_view(), name="projects_add_view"),
]