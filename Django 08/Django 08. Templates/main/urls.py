from django.urls import path, include

from main import views

urlpatterns = [
    path('', views.home),
    path('football/', views.football),
    path('hockey/', views.hockey),
    path('basketball/', views.basketball)
]
