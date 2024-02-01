from django.db import models
from rest_framework.exceptions import ValidationError

from account.models import User


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
