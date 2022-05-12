from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, ListView, UpdateView
from projects.models import Project
from .forms import NewRecordForm, RecordForm
from .models import Record


class RecordListView(LoginRequiredMixin, ListView):
    model = Record
    template_name = 'records/records_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(RecordListView, self).get_context_data(**kwargs)
        projects = Project.objects.filter(user_id=self.request.user.id)
        prefetch_projects = Prefetch('project', queryset=projects)
        context['records'] = Record.objects.prefetch_related(prefetch_projects)
        return context

    def post(self, request, *args, **kwargs):
        record_id = int(request.POST.get('id'))
        record = Record.objects.get(pk=record_id)
        record.endpoint = datetime.now()
        record.save()

        return redirect(reverse_lazy('records_list'))


class RecordView(LoginRequiredMixin, UpdateView):
    model = Record
    template_name = 'records/record.html'
    form_class = RecordForm
    success_url = reverse_lazy('records_list')

    def dispatch(self, request, *args, **kwargs):
        record = self.get_object()
        if record.endpoint is None:
            return redirect(RecordView.success_url)
        return super(RecordView, self).dispatch(request, *args, **kwargs)


class RecordAddView(LoginRequiredMixin, FormView):
    template_name = 'records/record_add.html'

    def get_context_data(self, **kwargs):
        form = NewRecordForm(self.request.POST or None)
        return {'form': form}

    def post(self, request, *args, **kwargs):
        form = NewRecordForm(request.POST)
        if form.is_valid():
            record = Record()
            record.project = form.cleaned_data["project"]
            if form.cleaned_data["start_right_now"]:
                record.startpoint = datetime.now()
            else:
                record.startpoint = form.cleaned_data["startpoint"]
            record.name = form.cleaned_data["name"]
            record.save()
        return redirect(reverse_lazy('records_list'))
