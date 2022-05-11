from datetime import datetime

from django.db.models import Prefetch
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin

from records.models import Record
from records.views import RecordListView
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


class ProjectView(LoginRequiredMixin, ListView):
    model = Record
    template_name = 'projects/project.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        id_ = self.kwargs.get('id')

        context = super(ProjectView, self).get_context_data(**kwargs)
        project = Project.objects.filter(user_id=self.request.user.id, id=id_)
        prefetch_projects = Prefetch('project', queryset=project)
        context['records'] = Record.objects.filter(project_id=id_).prefetch_related(prefetch_projects)
        context['title'] = project.first().name
        return context

    def post(self, request, **kwargs):
        project_id = kwargs.get('id')
        if 'project_delete' in request.POST:
            project = Project.objects.get(id=project_id)
            project.delete()
            return redirect(f'/projects/')
        record_id = int(request.POST.get('id'))
        record = Record.objects.get(pk=record_id)
        record.endpoint = datetime.now()
        record.save()
        return redirect(f'/projects/{project_id}/')
