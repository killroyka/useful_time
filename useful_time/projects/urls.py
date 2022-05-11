from django.urls import path
from .views import ProjectsListView, ProjectAddView
from records.views import RecordListView


urlpatterns = [
    path("", ProjectsListView.as_view(), name="projects_list"),
    path("add/", ProjectAddView.as_view(), name="projects_add"),
    path('<int:id>/', RecordListView.as_view(), name="project_records_list"),
]
