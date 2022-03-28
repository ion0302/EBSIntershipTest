from django.contrib import admin

from apps.tasks.models import Task, Comment, Timer, TimeLog

admin.site.register(Task)
admin.site.register(Comment)
admin.site.register(TimeLog)
admin.site.register(Timer)


