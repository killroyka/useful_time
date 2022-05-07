from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Project


class ProjectsListView(LoginRequiredMixin, TemplateView):
    template_name = "projects/projects_list.html"

    def get_context_data(self, **kwargs):
        projects = Project.objects.prefetch_related("records").filter(user_id=self.request.user.id)
        for project in projects:
            project.records = project.records.set()[5:]
        return {"projects": projects}
