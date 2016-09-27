from django.conf.urls import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                        url(r'^$','ugc.forwards.views.forwards_page'),
                        url(r'^list$','ugc.forwards.views.forwards_list'),
                        url(r'^parse/$', 'ugc.forwards.parse.parse_url'),
                        #url(r'^detail','ugc.forwards.views.forwards_detail'),
                       )
