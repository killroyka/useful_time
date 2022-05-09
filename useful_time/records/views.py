from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from projects.models import Project
from .forms import NewRecordForm
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

    def post(self, request):
        print(request.POST)
        record_id = int(request.POST.get('id'))
        record = Record.objects.get(pk=record_id)
        record.endpoint = datetime.now()
        record.save()
        return redirect(reverse_lazy('records_list'))


class RecordAddView(LoginRequiredMixin, CreateView):
    model = Record
    form_class = NewRecordForm
    template_name = 'records/record_add.html'
    success_url = reverse_lazy('records_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)