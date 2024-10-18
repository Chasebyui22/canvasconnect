from django.shortcuts import render
from .models import CanvasUser

def index(request):
    users = CanvasUser.objects.all()
    return render(request, 'index.html', {'users': users})
