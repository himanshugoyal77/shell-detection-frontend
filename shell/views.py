from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return render(request, 'shell/home.html')

def details(request):
    return render(request, 'shell/details.html')