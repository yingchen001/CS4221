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
from converter.xmljson import json_xml, xml_json
from converter.xmltables import *
from converter.jsontables import *
from converter.dbxml import *
from converter.dbjson import *
import showdb

def convert_post(request):
    outdict = {}
    if request.POST:
        try:
            inputTable = request.POST['input']
            method = request.POST['optradio']    
        except Exception as e:
            return render(request, "sorrypage.html")
            
        if method == 'JSON-XML':
            try:
                outdict['output'] = json_xml(inputTable)
            except Exception as e:
                return render(request,"sorrypage.html")

        elif method == 'XML-JSON':
            try:
                outdict['output'] = xml_json(inputTable)
            except Exception as e:
                return render(request,"sorrypage.html")

        elif method == 'XML-Relational':
            try:
                Contents.objects.all().delete()
                Attributes.objects.all().delete()
                Hierarchy.objects.all().delete()
                Elements.objects.all().delete()
                outdict['output'] = xml2db(inputTable)
            except Exception as e:
                return render(request,"sorrypage.html")

        elif method == 'Relational-XML':
            try:
                outdict['output'] = db2xml()                
            except Exception as e:
                return render(request,"sorrypage.html")

        elif method == 'JSON-Relational':
            try:
                Contents.objects.all().delete()
                Attributes.objects.all().delete()
                Hierarchy.objects.all().delete()
                Elements.objects.all().delete()  
                outdict['output'] = json2db(inputTable)
            except Exception as e:
                return render(request,"sorrypage.html")

        elif method == 'Relational-JSON':
            try:
                outdict['output'] = db2json()
            except Exception as e:
                return render(request,"sorrypage.html")
    return render(request, "home.html", outdict)

