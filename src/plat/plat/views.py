#!/usr/bin/python
# -*- coding:utf-8 -*-
# Create your views here.

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template.context import RequestContext
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.contrib.auth import logout
from django.conf import settings
        
@login_required
def home_page(request):
    return HttpResponseRedirect("/accounts/login/")

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/")

@login_required
def main(request):
    return render_to_response('index.html')

def forbidden(request):
    return render_to_response("forbidden.html")

