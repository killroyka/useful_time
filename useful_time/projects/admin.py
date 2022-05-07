from django.contrib import admin

from projects.models import Project


@admin.register(Project)
class RecordAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')
