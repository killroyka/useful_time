import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch, QuerySet, Q
from django.db.models import Sum, Min, Max, Count
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, ListView, UpdateView
from projects.models import Project

from .forms import NewRecordForm, RecordForm
from .models import Record, SubRecord


class RecordListView(LoginRequiredMixin, ListView):
    model = Record
    template_name = 'records/records_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(RecordListView, self).get_context_data(**kwargs)
        projects = Project.objects.filter(user_id=self.request.user.id)
        prefetch_projects = Prefetch('project', queryset=projects)

        records = Record.objects \
            .prefetch_related(prefetch_projects) \
            .prefetch_related("subrecords") \
            .filter(project__in=projects) \
            .annotate(longitude=Sum("subrecords__longitude"),
                      startpoint=Min("subrecords__startpoint"),
                      endpoint=Max("subrecords__endpoint"),
                      is_end=Count("subrecords",
                                   filter=Q(subrecords__endpoint=None))) \
            .order_by("endpoint")
        context['records'] = records
        return context

    def post(self, request, *args, **kwargs):
        """Метод POST, обрабатывающий разные виды запроса (пауза,
        старт таймера) и создающий соответствующие изменения в базе данных.
        """

        record_id = int(request.POST.get('id'))
        print(datetime.datetime.now())
        if 'stop_timer' in request.POST:
            sub_record = SubRecord.objects.filter(record_id=record_id, endpoint=None).first()
            sub_record.endpoint = datetime.datetime.now()
            sub_record.longitude = sub_record.get_back_longitude
            sub_record.endpoint = datetime.datetime.now()
            sub_record.save()

        elif 'continue_timer' in request.POST:
            record = Record.objects.get(pk=record_id)
            sub_record = SubRecord(
                record=record,
                startpoint=datetime.datetime.now()
            )
            sub_record.save()

        return redirect(reverse_lazy('records_list'))


class RecordView(LoginRequiredMixin, UpdateView):
    model = Record
    template_name = 'records/record.html'
    form_class = RecordForm
    success_url = reverse_lazy('records_list')

    def get_object(self, queryset=None):
        prefetch_user = Prefetch('user', queryset=QuerySet(self.request.user))
        projects = Project.objects \
            .prefetch_related(prefetch_user) \
            .filter(user_id=self.request.user) \
            .only('name')

        prefetch_projects = Prefetch('project', queryset=projects)
        record = Record.objects. \
            prefetch_related(prefetch_projects). \
            get(pk=self.kwargs['pk'])

        return record

    def get_context_data(self, **kwargs):
        context = dict()
        form = self.get_form()

        form.fields['project'].queryset = form.fields['project'] \
            .queryset.filter(user_id=self.request.user.id)

        sub_records = SubRecord.objects.filter(record_id=self.object.id)

        context['form'] = form
        context['sub_records'] = sub_records

        return context

    def post(self, request, *args, **kwargs):
        """Метод POST, который удаляет запись если есть соответсвующий
         запрос, иначе вызывает метод 'родителя'.
         """
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
        """Метод POST, создающий таймер в базе данных"""

        form = RecordAddView.form_class(request.POST)
        if form.is_valid():
            record = Record()
            record.project = form.cleaned_data["project"]
            record.name = form.cleaned_data["name"]
            record.save()
            sub_record = SubRecord()
            sub_record.record = record
            sub_record.startpoint = datetime.datetime.now()
            sub_record.save()
        return redirect(reverse_lazy('records_list'))
