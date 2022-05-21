from django.contrib import admin

from records.models import Record, SubRecord


@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    list_display = ('project', 'name')


@admin.register(SubRecord)
class RecordAdmin(admin.ModelAdmin):
    list_display = ("record", "startpoint", "endpoint")
