from django.urls import path

from . import views
from .views import AboutPageView

app_name = 'notes'
urlpatterns = [
    path("", views.notes_list, name="notes_list"),
    path("<int:note_id>/", views.note_detail, name="note_detail"),
    # path('about/', views.about, name='about'),
    path("create/", views.create_note, name="note_create"),
    path("about/", AboutPageView.as_view(), name="about"),

]