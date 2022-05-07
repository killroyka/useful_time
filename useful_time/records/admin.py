from django.contrib import admin

from records.models import Record


@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    list_display = ('project', 'name')
