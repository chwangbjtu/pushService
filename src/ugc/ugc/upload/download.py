#!/usr/bin/python
# -*- coding:utf-8 -*-

from django.http import HttpResponseRedirect,HttpResponse,HttpResponseNotFound
from django.shortcuts import render_to_response
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.core.cache import cache

import ugc.settings
import os.path
import error
from ugc.log import masterlogging
from ugc.log import logginghelper
import utils

def get_uploaded_file(request):
    if not request.GET.has_key("filename"):
        return HttpResponse(status=400)
    filename = request.GET["filename"]
    full_path = "%s/%s" % (settings.FILE_UPLOAD_TEMP_DIR,filename)
    if not os.path.exists(full_path):
        return HttpResponseNotFound('<h1>File not exists</h1>')
    if not os.access(full_path, os.R_OK):
        return HttpResponse(status=500)
    return bigFileView(full_path)

def bigFileView(filename):
    def readFile(fn, buf_size=262144):
        try:
            file_handler = open(fn, "rb")
            while True:
                content = file_handler.read(buf_size)
                if content:
                    yield content
                else:
                    break
            file_handler.close()
        except Exception,e:
            masterlogging.error(logginghelper.LogicLog("None","DownloadFile","except",str(e)))
            return
    file_length = os.path.getsize(filename)
    response = HttpResponse(readFile(filename),content_type="application/octet-stream")
    response["Content-Length"] = str(file_length)
    return response