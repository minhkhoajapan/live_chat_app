from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password

# Create your models here.
class Message(models.Model):
    message = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to='files/', blank=True, null=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    room_name = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

class ChatRoom(models.Model):
    room_name = models.CharField(max_length=255, null=False, unique=True)
    password = models.CharField(max_length=128)
    authenticated_member = models.ManyToManyField(User, related_name="chatrooms")

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
    
    def verify_password(self, raw_password):
        return check_password(raw_password, self.password)
    

