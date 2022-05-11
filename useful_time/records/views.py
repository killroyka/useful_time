from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView
from projects.models import Project
from .forms import NewRecordForm, RecordForm
from .models import Record


class RecordListView(LoginRequiredMixin, ListView):
    model = Record
    template_name = 'records/records_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        id_ = self.kwargs.get('id')

        context = super(RecordListView, self).get_context_data(**kwargs)
        if id_:
            project = Project.objects.filter(user_id=self.request.user.id, id=id_)
            prefetch_projects = Prefetch('project', queryset=project)
            context['records'] = Record.objects.filter(project_id=id_).prefetch_related(prefetch_projects)
            context['title'] = f'Записи в "{project.all()[0].name}"'
        else:
            projects = Project.objects.filter(user_id=self.request.user.id)
            prefetch_projects = Prefetch('project', queryset=projects)
            context['records'] = Record.objects.prefetch_related(prefetch_projects)
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

        if project_id:
            return redirect(f'/projects/{project_id}/')
        else:
            return redirect(reverse_lazy('records_list'))


class RecordView(LoginRequiredMixin, UpdateView):
    model = Record
    template_name = 'records/record.html'
    form_class = RecordForm
    success_url = reverse_lazy('records_list')

    def get_form(self, form_class=None):
        form = super(RecordView, self).get_form(form_class=RecordView.form_class)
        record_object = self.get_object()

        attrs = form.fields['startpoint'].widget.attrs
        attrs['value'] = str(record_object.startpoint.replace(microsecond=0).isoformat())
        form.fields['startpoint'].widget.__init__(attrs=attrs)

        if record_object.endpoint:
            attrs = form.fields['endpoint'].widget.attrs
            attrs['value'] = str(record_object.endpoint.replace(microsecond=0).isoformat())
            form.fields['endpoint'].widget.__init__(attrs=attrs)

        return form


class RecordAddView(LoginRequiredMixin, CreateView):
    model = Record
    form_class = NewRecordForm
    template_name = 'records/record_add.html'
    success_url = reverse_lazy('records_list')
