from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Movie(models.Model):
    STATUS_CHOICES = [
        ('planned', 'Хочу посмотреть'),
        ('watching', 'Смотрю'),
        ('watched', 'Посмотрел')
    ]

    title = models.CharField(max_length=100, unique=True)
    genre = models.ForeignKey(Genre, on_delete=models.PROTECT, related_name='movies')
    release_year = models.PositiveIntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='planned')
    rating = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)],null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='movies')
