from django.shortcuts import render
from .models import CanvasUser

def index(request):
    users = CanvasUser.objects.all()
    return render(request, 'index.html', {'users': users})
# views.py
from django.http import JsonResponse
import csv

def upload_csv(request):
    if request.method == 'POST' and request.FILES['file']:
        csv_file = request.FILES['file']
        decoded_file = csv_file.read().decode('utf-8').splitlines()
        reader = csv.reader(decoded_file)

        data = []
        for row in reader:
            data.append(row)  # Process CSV data and add to list

        return JsonResponse({'data': data})  # Send data back to the front end
    return JsonResponse({'error': 'Invalid request'}, status=400)

