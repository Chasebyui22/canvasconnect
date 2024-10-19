from django.shortcuts import render
from .models import CanvasUser

def index(request):
    users = CanvasUser.objects.all()
    return render(request, 'index.html', {'users': users})
# views.py
# from django.http import JsonResponse
# import csv

# def upload_csv(request):
#     if request.method == 'POST' and request.FILES['file']:
#         csv_file = request.FILES['file']
#         decoded_file = csv_file.read().decode('utf-8').splitlines()
#         reader = csv.reader(decoded_file)

#         data = []
#         for row in reader:
#             data.append(row)  # Process CSV data and add to list

#         return JsonResponse({'data': data})  # Send data back to the front end
#     return JsonResponse({'error': 'Invalid request'}, status=400)

# views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .process_csv import *  # Import your function

@csrf_exempt  # Use this if you're not handling CSRF tokens in your AJAX call
def upload_csv(request):
    if request.method == 'POST' and request.FILES.get('file'):
        csv_file = request.FILES['file']
        
        # Process the CSV using your external function
        new_csv_data = process_csv_from_django(csv_file.read().decode('utf-8'))  # Ensure you decode the bytes

        # Return the new CSV data as a response
        return JsonResponse({'data': new_csv_data})

    return JsonResponse({'error': 'Invalid request'}, status=400)
