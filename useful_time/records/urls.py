from django.urls import path
from .views import RecordAddView, RecordListView, RecordView

urlpatterns = [
    path('', RecordListView.as_view(), name='records_list'),
    path('add/', RecordAddView.as_view(), name='record_add'),
    path('<int:pk>/', RecordView.as_view(), name='record')
]
