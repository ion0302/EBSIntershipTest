# Generated by Django 3.2.12 on 2022-03-25 14:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0008_task_work_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='work_time',
        ),
    ]