from django.http import HttpResponse
from django.shortcuts import render
import datetime

def current_day(request):
    day = datetime.datetime.now().strftime("%A")
    return HttpResponse(f"Today is {day}")
