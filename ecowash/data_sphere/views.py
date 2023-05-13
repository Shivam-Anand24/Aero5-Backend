from django.shortcuts import render
from django.http import JsonResponse


def home_view(request):
    return JsonResponse({'message': 'App is working!'})


