from django.contrib import admin

from apps.tasks.models import Task, Comment, Log

admin.site.register(Task)
admin.site.register(Comment)
admin.site.register(Log)

