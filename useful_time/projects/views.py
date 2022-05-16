from datetime import datetime

from django.db.models import Prefetch
from django.urls import reverse_lazy
from django.http import Http404
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from records.models import Record
from .models import Project
from .forms import ProjectForm
from django.shortcuts import redirect


class ProjectsListView(LoginRequiredMixin, TemplateView):
    template_name = "projects/projects_list.html"

    def get_context_data(self, **kwargs):
        records = Record.objects.all()
        prefetch_records = Prefetch("records", queryset=records)
        projects = Project.objects.prefetch_related("user", prefetch_records) \
            .filter(user_id=self.request.user.id).only("id", "name", "description", "color", "user_id")
        return {"projects": projects}


class ProjectAddView(LoginRequiredMixin, FormView):
    template_name = "projects/project_add.html"

    def get_context_data(self, **kwargs):
        project_form = ProjectForm(self.request.POST or None)
        return {'form': project_form}

    def post(self, request, *args, **kwargs):
        project_form = ProjectForm(request.POST)
        if project_form.is_valid():
            project = Project()
            project.user = request.user
            project.name = project_form.cleaned_data["name"]
            project.description = project_form.cleaned_data["description"]
            project.color = project_form.cleaned_data["color"].upper()
            project.save()
            return redirect('/projects')
        return redirect('/projects/add')


class ProjectView(LoginRequiredMixin, TemplateView):
    model = Record
    template_name = 'projects/project.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        pk = self.kwargs.get('pk')

        context = super(ProjectView, self).get_context_data(**kwargs)
        project = Project.objects.get(id=pk)

        if project is None:
            return None
        if self.request.user.id != project.user_id:
            return None

        context['records'] = Record.objects.filter(project_id=pk)
        context['title'] = project.name
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if context is None:
            raise Http404()
        return self.render_to_response(context)

    def post(self, request, **kwargs):
        project_id = kwargs.get('pk')
        if 'project_delete' in request.POST:
            project = Project.objects.get(id=project_id)
            project.delete()
            return redirect(f'/projects/')
        elif 'project_edit' in request.POST:
            return redirect(f'/projects/{project_id}/edit/')
        record_id = int(request.POST.get('id'))
        record = Record.objects.get(pk=record_id)
        record.endpoint = datetime.now()
        record.save()
        return redirect(f'/projects/{project_id}/')


class ProjectEditView(LoginRequiredMixin, UpdateView):
    model = Project
    template_name = 'projects/project_edit.html'
    form_class = ProjectForm
    success_url = reverse_lazy('projects_list')

    def dispatch(self, request, *args, **kwargs):
        project = self.get_object()
        if project.user.id != request.user.id:
            raise Http404()
        return super().post(request, *args, **kwargs)
