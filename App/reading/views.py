from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .models import Reading
from django.db import IntegrityError
# Create your views here.
def index(request):
    return render(request,'base.html',context={'text':'hello'})

@csrf_exempt
def add_reading(request):
    if request.method == 'POST':
        raw_data = request.body.decode('utf-8')
        json_data = json.loads(raw_data)
        reading_instance = Reading(
            temperature_data=json_data['temp'],
            pressure_data=json_data['pressure'],
            moisture_data=json_data['moisture']
        )
        try:
            reading_instance.save()
            return JsonResponse({'message':'Data Saved'},status=201)
        except IntegrityError as e:
            return JsonResponse({'error': 'Unable to save data'}, status=422)