# -*- coding: utf-8 -*-
 
from django.shortcuts import render
from django.views.decorators import csrf
 
import optparse
import sys
import os

from django.http import HttpResponse

def back_post(request):
    return render(request, "home.html")