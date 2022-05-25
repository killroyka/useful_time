from datetime import datetime

from dateutil.tz import tzlocal
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch, Q
from django.db.models import Sum, Min, Max, Count
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView, UpdateView
from records.models import Record, SubRecord
from useful_time.settings import DATE_INPUT_FORMATS

from .forms import ProjectForm
from .models import Project


class ProjectsListView(LoginRequiredMixin, TemplateView):
    """
    Отрисовка шаблона состоящего из списка проектов.
    """
    template_name = "projects/projects_list.html"

    def get_context_data(self, **kwargs):
        records = Record.objects.all()
        prefetch_records = Prefetch("records", queryset=records)
        projects = Project.objects.prefetch_related(prefetch_records) \
            .filter(user_id=self.request.user.id).only(
            "id", "name", "description", "color", "user_id"
        )
        return {"projects": projects}


class ProjectAddView(LoginRequiredMixin, FormView):
    """
    Отрисовка шаблона добавления проекта.
    """
    template_name = "projects/project_add.html"

    def get_context_data(self, **kwargs):
        project_form = ProjectForm(self.request.POST or None)
        return {'form': project_form}

    def post(self, request, *args, **kwargs):
        project_form = ProjectForm(request.POST)
        print(type(project_form))
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
    """
    Отрисовка шаблона проекта.
    """
    model = Record
    template_name = 'projects/project.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        """
        Контекст шаблона, если возвращает None,
        значит, что проект пользоваьелю не принадлежит.
        """
        pk = self.kwargs.get('pk')

        context = super(ProjectView, self).get_context_data(**kwargs)
        project = Project.objects.get(id=pk)

        if project is None:
            return None
        if self.request.user.id != project.user_id:
            return None

        context['project'] = project
        context['records'] = Record.objects. \
            prefetch_related("subrecords") \
            .annotate(longitude=Sum("subrecords__longitude"),
                      startpoint=Min("subrecords__startpoint"),
                      endpoint=Max("subrecords__endpoint"),
                      is_end=Count(
                          "subrecords",
                          filter=Q(subrecords__endpoint=None)
                      )) \
            .filter(project_id=pk) \
            .order_by("endpoint")

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
            return redirect('/projects/')
        elif 'project_edit' in request.POST:
            return redirect(f'/projects/{project_id}/edit/')
        record_id = int(request.POST.get('id'))
        if 'stop_timer' in request.POST:
            sub_record = SubRecord.objects.filter(
                record_id=record_id, endpoint=None
            ).first()
            sub_record.endpoint = datetime.now(tzlocal())
            sub_record.longitude = sub_record.get_back_longitude
            sub_record.endpoint = datetime.now(tzlocal()) \
                .strftime(DATE_INPUT_FORMATS[0])

            sub_record.save()
        elif 'continue_timer' in request.POST:
            record = Record.objects.get(pk=record_id)
            sub_record = SubRecord(
                record=record,
                startpoint=datetime.now(tzlocal()).strftime(
                    DATE_INPUT_FORMATS[0]
                )
            )
            sub_record.save()
        return redirect(f'/projects/{project_id}/')


class ProjectEditView(LoginRequiredMixin, UpdateView):
    """
    Отрисовка шаблона изменения проекта.
    """
    model = Project
    template_name = 'projects/project_edit.html'
    form_class = ProjectForm
    success_url = reverse_lazy('projects_list')

    def dispatch(self, request, *args, **kwargs):
        """Dispatch, проверящий на принадлежность выбранного проекта
        текушему пользователю. Возвращает 404, если пользоваьтель не совпал.
        """
        project = self.get_object()
        if project.user.id != request.user.id:
            raise Http404()
        return super().post(request, *args, **kwargs)
