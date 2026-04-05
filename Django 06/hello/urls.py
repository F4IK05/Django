from django.urls import path
from hello.views import say_hello

urlpatterns = [
    path('', say_hello)
]