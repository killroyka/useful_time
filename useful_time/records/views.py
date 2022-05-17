from datetime import datetime

from dateutil.tz import tzlocal
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch, QuerySet
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import FormView, ListView, UpdateView
from projects.models import Project
from .forms import NewRecordForm, RecordForm
from .models import Record, SubRecord
from useful_time.settings import DATE_INPUT_FORMATS


class RecordListView(LoginRequiredMixin, ListView):
    model = Record
    template_name = 'records/records_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(RecordListView, self).get_context_data(**kwargs)
        projects = Project.objects.filter(user_id=self.request.user.id)
        prefetch_projects = Prefetch('project', queryset=projects)

        records = Record.objects.prefetch_related(prefetch_projects).filter(project__in=projects)
        prefetch_records = Prefetch('record', queryset=records)

        sub_records = SubRecord.objects.prefetch_related(prefetch_records).filter(record__in=records, endpoint=None)
        records_and_sub_records = {record.id: None for record in records}

        for sub_record in sub_records:
            if sub_record.record_id in records_and_sub_records:
                records_and_sub_records[sub_record.record_id] = sub_record
        context['records'] = records
        context['sub_records'] = records_and_sub_records

        return context

    def post(self, request, *args, **kwargs):
        record_id = int(request.POST.get('id'))
        if 'stop_timer' in request.POST:
            sub_record = SubRecord.objects.filter(record_id=record_id, endpoint=None)[0]
            sub_record.endpoint = datetime.now(tzlocal()).strftime(DATE_INPUT_FORMATS[0])
            sub_record.save()
        elif 'continue_timer' in request.POST:
            record = Record.objects.get(pk=record_id)
            sub_record = SubRecord(
                record=record,
                startpoint=datetime.now(tzlocal()).strftime(DATE_INPUT_FORMATS[0])
            )
            sub_record.save()
        else:
            dt = datetime.now(tzlocal()).strftime(DATE_INPUT_FORMATS[0])

            record = Record.objects.get(pk=record_id)
            record.endpoint = dt
            record.save()

        return redirect(reverse_lazy('records_list'))


class RecordView(LoginRequiredMixin, UpdateView):
    model = Record
    template_name = 'records/record.html'
    form_class = RecordForm
    success_url = reverse_lazy('records_list')

    def get_object(self, queryset=None):
        prefetch_user = Prefetch('user', queryset=QuerySet(self.request.user))
        projects = Project.objects.prefetch_related(prefetch_user).filter(user_id=self.request.user).only('name')
        prefetch_projects = Prefetch('project', queryset=projects)
        record = Record.objects.prefetch_related(prefetch_projects).get(pk=self.kwargs['pk'])
        return record

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.endpoint is None or self.object.project.user.id != self.request.user.id:
            return redirect(RecordView.success_url)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = dict()
        form = self.get_form()

        form.fields['project'].queryset = form.fields['project'].queryset.filter(user_id=self.request.user.id)
        sub_records = SubRecord.objects.filter(record_id=self.object.id)

        context['form'] = form
        context['sub_records'] = sub_records

        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        if self.object.endpoint is None or self.object.project.user.id != self.request.user.id:
            return redirect(RecordView.success_url)
        return render(request, RecordView.template_name, context=context)

    def post(self, request, *args, **kwargs):
        if 'record_delete' in request.POST:
            record = Record.objects.get(id=kwargs['pk'])
            record.delete()
            return redirect(RecordView.success_url)
        return super().post(request, *args, **kwargs)


class RecordAddView(LoginRequiredMixin, FormView):
    template_name = 'records/record_add.html'
    form_class = NewRecordForm

    def get_context_data(self, **kwargs):
        form = RecordAddView.form_class(self.request.POST or None)
        queryset = Project.objects.filter(user_id=self.request.user.id)
        form.fields['project'].__init__(queryset)
        return {'form': form}

    def post(self, request, *args, **kwargs):
        form = RecordAddView.form_class(request.POST)
        if form.is_valid():
            record = Record()
            record.project = form.cleaned_data["project"]
            if form.cleaned_data["start_right_now"]:
                record.startpoint = datetime.now(tzlocal()).strftime(DATE_INPUT_FORMATS[0])
            else:
                record.startpoint = form.cleaned_data["startpoint"]
            record.name = form.cleaned_data["name"]
            record.save()
            sub_record = SubRecord(
                record=record,
                startpoint=record.startpoint
            )
            sub_record.save()
        return redirect(reverse_lazy('records_list'))
