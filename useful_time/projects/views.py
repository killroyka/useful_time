from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Project
from .forms import NewProjectForm
from django.shortcuts import redirect


class ProjectsListView(LoginRequiredMixin, TemplateView):
    template_name = "projects/projects_list.html"

    def get_context_data(self, **kwargs):
        projects = Project.objects.prefetch_related("records").filter(user_id=self.request.user.id)
        return {"projects": projects}


class ProjectAddView(LoginRequiredMixin, FormView):
    template_name = "projects/project_add.html"

    def get_context_data(self, **kwargs):
        project_form = NewProjectForm(self.request.POST or None)
        return {'form': project_form}

    def post(self, request, *args, **kwargs):
        project_form = NewProjectForm(request.POST)

        # TODO: если цвет невалиден, идет редирект и форма очищается, а нужно просто уведомлять
        #  об ошибке и не сбрасывать форму, (нужна промощь)
        if project_form.is_valid():
            project = Project()
            project.user = request.user
            project.name = project_form.cleaned_data["name"]
            project.description = project_form.cleaned_data["description"]
            project.color = project_form.cleaned_data["color"].upper()
            project.save()
            return redirect('/projects')
        return redirect('/projects/add')
