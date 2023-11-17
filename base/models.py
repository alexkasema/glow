from django.db import models
from django.contrib.auth import get_user_model #! gets the model of the currently authenticated user

User = get_user_model()
# Create your models here.

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) #! foreign key that links to user model
    id_user = models.IntegerField()  #! the id of the user that owns this profile
    bio = models.TextField(blank=True)
    profile_img = models.ImageField(upload_to = 'profile_images', default='avatar.svg')
    location = models.CharField(max_length=100, blank=True)

    def __str__(self) -> str:
        return self.user.username

