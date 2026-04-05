from django.urls import path

from quotes.views import random_quote

urlpatterns = [
    path('', random_quote)
]