
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from config import settings
from .models import Comment, Task


def comment_mail_send(user):
    subject = 'Task Notification'
    message = f'Hi {user.username}, a new comment is attached to your task.'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user.email]
    send_mail(subject, message, email_from, recipient_list, fail_silently=False)


def task_mail_send(user):
    subject = 'Task Notification'
    message = f'Hi {user.username}, a new task is attached to you.'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user.email]
    send_mail(subject, message, email_from, recipient_list, fail_silently=False)


@receiver(post_save, sender=Comment)
def comment_send_mail(sender, instance, created, **kwargs):
    if created:
        task = instance.task
        user = task.assigned_to
        if user:
            comment_mail_send(user)


@receiver(post_save, sender=Task)
def task_send_mail(sender, instance, created, **kwargs):
    if created:
        user = instance.assigned_to
        if user:
            task_mail_send(user)
