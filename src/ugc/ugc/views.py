#!/usr/bin/python
# -*- coding:utf-8 -*-

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

@login_required
def home_page(request):
	return HttpResponseRedirect("/audit/")

def logout_sys(request):
    logout(request)
    return HttpResponseRedirect("/")


def forbidden(request):
    return render_to_response("forbidden.html",{})