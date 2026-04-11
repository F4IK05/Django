from django.shortcuts import render

def home(request):
    return render(request, 'base/home.html')

def football(request):
    return render(request, 'football/football.html')

def hockey(request):
    return render(request, 'hockey/hockey.html')

def basketball(request):
    return render(request, 'basketball/basketball.html')