#!/usr/bin/python
# -*- coding:utf-8 -*-

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.conf import settings
from django.contrib.auth.decorators import login_required

@login_required
def play_video(request):
    if request.GET.has_key("video"):
        video_url = request.GET["video"]
    else:
        return render_to_response("error.html",{"error":"无效视频地址"})
    if request.GET.has_key("player"):
        player_type = request.GET["player"]
    else:
        player_type = "html5"
    player_html = ""
    if player_type == "html5":
        player_html = "play_video_with_html5.html"
    elif player_type == "wmplayer":
        player_html = "play_video_with_wmplayer.html"
    elif player_type == "flash":
        player_html = "play_video_with_flash.html"
    else:
        player_html = "play_video_with_html5.html"
    return render_to_response(player_html,{"video_url":video_url})