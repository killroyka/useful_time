from django.urls import path
from .views import RecordAddView, RecordListView

urlpatterns = [
    path('', RecordListView.as_view(), name='records_list'),
    path('add/', RecordAddView.as_view(), name='record_add')
]
