from django.conf.urls import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       url(r"^$","ugc.show.views.show_video",name = "show_video"),
                       url(r"^unaudit$","ugc.show.views.show_unaudit",name = "show_unaudit"),
                       )
