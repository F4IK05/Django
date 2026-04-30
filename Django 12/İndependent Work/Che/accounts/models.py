from django.db import models
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    bio = models.TextField('О себе', blank=True, null=True)
    avatar = CloudinaryField('avatar', blank=True, null=True)

    def __str__(self):
        return self.username