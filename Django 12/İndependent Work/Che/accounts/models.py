from django.db import models
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    bio = models.TextField('О себе', blank=True, null=True)
    avatar = CloudinaryField('avatar', blank=True, null=True)

    is_banned = models.BooleanField(default=False)

    @property
    def is_admin(self):
        return self.is_staff or self.is_superuser

    def __str__(self):
        return self.username

class Notification(models.Model):
    class Type(models.TextChoices):
        ARTICLE_PENDING = 'pending', 'Статья на модерации'
        ARTICLE_APPROVED = 'approved', 'Статья одобрена'
        ARTICLE_REJECTED = 'rejected', 'Статья отклонена'

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notifications')

    type = models.CharField(max_length=20, choices=Type.choices)

    article_title = models.CharField(max_length=100)
    article_id = models.IntegerField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user} — {self.type}'