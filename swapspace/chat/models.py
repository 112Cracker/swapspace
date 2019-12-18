from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ChatRoom(models.Model):
    roomname = models.CharField(max_length=200)
    # A chatroom is restricted to two users
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='host1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='host2')


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    roomname = models.CharField(max_length=200)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content