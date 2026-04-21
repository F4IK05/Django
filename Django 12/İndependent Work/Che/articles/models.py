from cloudinary import CloudinaryImage
from cloudinary.models import CloudinaryField
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=100)

    author = models.CharField(max_length=100)

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='articles'
    )

    image = CloudinaryField('image')
    content = models.TextField()

    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def mini_content(self):
        return self.content[:50] + "...."

    def __str__(self):
        return self.title