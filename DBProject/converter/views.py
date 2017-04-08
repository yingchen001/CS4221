#coding:utf-8
from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
# from django.http import JsonResponse
 
def index(request):
    return HttpResponse(u"XML-JSON Converter")

def home(request):
    return render(request, 'home.html')
