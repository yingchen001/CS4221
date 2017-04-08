# -*- coding: utf-8 -*-
 
from django.shortcuts import render
from django.views.decorators import csrf
 
import optparse
import sys
import os

from django.http import HttpResponse

def showmanual(request):
    return render(request, "manual.html")