from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.http import HttpResponse

from .spark.data_processing import process_csv
from .models import User
from .data_service import DataService
from .db_to_json_converter import DBToJsonConverter

import json
import os


@csrf_exempt
def process_file(request):
     if request.method == 'POST' and request.FILES['csv_file']:
        csv_file = request.FILES['csv_file']
        file_name = csv_file.name
        file_path = os.path.join(settings.MEDIA_ROOT, 'temp', file_name)
        print('------------@@------------', file_path)

        # Create the directory if it doesn't exist
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Create the empty file
        open(file_path, 'wb').close()

        # Save the uploaded file temporarily
        with open(file_path, 'wb') as destination:
            for chunk in csv_file.chunks():
                destination.write(chunk)

        print('------------@@------------', file_path)
        # Process the CSV file
        success = process_csv(file_path, request.POST['key'])

        # Delete the temporary file
        os.remove(file_path)

        if success:
            return HttpResponse('Done')
        else:
            return HttpResponse('Error')
     else:

        return render(request, 'process_file.html')



def home_view(request):
    return JsonResponse({'message': 'App is working!'})



@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')

        print('------------------', email, password)
        print('------------------', data)
        try:
            user = User.objects.get(email=email, password=password)
            data = {
                'token': user.token,
                'role': user.role.id
            }
            return JsonResponse(data, status=200)
        except User.DoesNotExist:
            return JsonResponse({'message': 'Login failed'}, status=401)
    else:
        return JsonResponse({'message': 'Invalid request'}, status=400)
    




@csrf_exempt
def get_data_view(request, table_name):
    data_service = DataService()
    df = data_service.read_data(table_name)
    
    # Assuming the DataFrame has columns and rows data
    headers = df.columns
    data = df.collect()

    converted_data = {
        'headers': headers,
        'data': [row.asDict() for row in data]
    }

    return JsonResponse(converted_data)