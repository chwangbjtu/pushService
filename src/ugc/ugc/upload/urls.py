from django.conf.urls import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),

#   url(r'^static/(?P<path>.*)$', 'django.views.static.serve',{'document_root':settings.STATIC_ROOT}),
    url(r'^$','ugc.upload.views.home_page'),
    url(r'^upload/$','ugc.upload.views.upload_video'),
    url(r'^finish_upload','ugc.upload.views.finish_upload'),
    url(r"^upload_list/","ugc.upload.uplist.upload_list", name = "upload_list"),
    url(r"^download/","ugc.upload.download.get_uploaded_file"),
)
