# -*- coding: utf-8 -*-
 
from django.shortcuts import render
from django.views.decorators import csrf
 
import optparse
import sys
import os

from django.http import HttpResponse
from converter.models import *
from page import page
from sorrypage import sorrypage

def showtables(request):
    table1 = Elements.objects.all()
    table2 = Hierarchy.objects.all()
    table3 = Attributes.objects.all()
    table4 = Contents.objects.all()
    rst = page(table1, table2, table3, table4)
    return HttpResponse(rst)