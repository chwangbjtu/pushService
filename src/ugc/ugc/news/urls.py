from django.conf.urls import patterns, include, url
from django.conf import settings


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ugc.views.home', name='home'),
    # url(r'^ugc/', include('ugc.ugc.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^add$','ugc.news.views.add_news'),
)