from django.urls import path

from weekday.views import current_day

urlpatterns = [
    path('', current_day)
]