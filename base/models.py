from django.db import models
from django.contrib.auth import get_user_model #! gets the model of the currently authenticated user

import uuid

from datetime import datetime

User = get_user_model()
# Create your models here.

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) #! foreign key that links to user model
    id_user = models.IntegerField()  #! the id of the user that owns this profile
    bio = models.TextField(blank=True)
    profile_img = models.ImageField(null=True, upload_to = 'profile', default='legolas.jpg')
    location = models.CharField(max_length=100, blank=True)

    def __str__(self) -> str:
        return self.user.username


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.CharField(max_length=100) #! name of user the post belongs to
    image = models.ImageField(upload_to='post_images')
    caption = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)
    no_of_likes = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.user