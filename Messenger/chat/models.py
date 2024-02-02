import jdatetime
from django.db import models
from rest_framework.exceptions import ValidationError

from account.models import User
from jdatetime import datetime as jdatetime


class Chat(models.Model):
    users = models.ManyToManyField(User)
    created_at = models.DateTimeField(auto_now_add=True)



class Group(Chat):
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='sent_messages', null=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)

    def jalali_time(self):
        shamsi_date = jdatetime.fromgregorian(datetime=self.created_at)
        return shamsi_date.strftime("%H:%M")