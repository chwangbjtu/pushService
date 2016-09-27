from django.conf.urls import patterns, include, url
# import plat.subscribe
# from plat.subscribe.views import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
from django.contrib.auth.models import Permission
admin.site.register(Permission)

urlpatterns = patterns('',
    
    # Uncomment the admin/doc line below to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    
    # login
    url(r'^accounts/login/$','django.contrib.auth.views.login',{'template_name':'login.html'}),
    url(r'^accounts/logout/$','plat.views.logout'),
    url(r'^$', 'plat.views.home_page'),

    #main
    url(r'^main/', 'plat.views.main', name = 'main'),

    #subscribe
    url(r'^subscribe/',include('subscribe.urls')),
    #video_house
    url(r'^video_house/',include('video_house.urls')),
    #blacklist
    url(r'^blacklist/',include('blacklist.urls')),
    #api
    url(r'^api/',include('api.urls')),
    #forbidden
    url(r'^forbidden/$','plat.views.forbidden', name = 'forbidden'),
    #repost
    url(r'^repost/',include('repost.urls')),
    #xvsync
    url(r'^xvsync/',include('xvsync.urls')),
    
)
