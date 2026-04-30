from django.urls import path

from movies.views import movie_list, add_movie, edit_movie, delete_movie

urlpatterns = [
    path('', movie_list, name='movie_list'),
    path('add/', add_movie, name='add_movie'),
    path('edit/<int:id>/', edit_movie, name='edit_movie'),
    path('delete/<int:id>/', delete_movie, name='delete_movie'),
]