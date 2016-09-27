#!/bin/env python
# -*- coding: utf-8    -*- 
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.conf import settings

def  main_enter(request):
   
    return render_to_response("ask_task_num.html")

