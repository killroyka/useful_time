from django.urls import path
from .views import ProjectsListView, ProjectAddView, ProjectView


urlpatterns = [
    path("", ProjectsListView.as_view(), name="projects_list"),
    path("add/", ProjectAddView.as_view(), name="project_add"),
    path('<int:id>/', ProjectView.as_view(), name="project_records_list"),
]
