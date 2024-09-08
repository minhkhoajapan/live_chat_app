from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Message(models.Model):
    message = models.TextField()
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    room_name = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)