from django.conf.urls import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from django.contrib.auth.models import Permission
admin.site.register(Permission)

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ugc.views.home', name='home'),
    # url(r'^ugc/', include('ugc.ugc.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^$','ugc.views.home_page'),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$','django.contrib.auth.views.login',{'template_name':'login.html'}),
    url(r'^accounts/logout/$','ugc.views.logout_sys'),
    url(r'^forbidden/$','ugc.views.forbidden'),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve',{'document_root':settings.STATIC_ROOT}),
    url(r'^audit/', include('ugc.audit.urls')),
    url(r'^upload/',include('ugc.upload.urls')),
    url(r'^forwards/', include('ugc.forwards.urls')),
    url(r'^news/',include('ugc.news.urls')),
    url(r'^show/',include('ugc.show.urls')),
    #url(r'^maze', include('ugc.maze.urls')),
    #url(r"^audit/asktask", "ugc.audit.ask_task_num.ask_task_num", name = "ask_task_num"),
    #url(r"^audit/viewtask", "ugc.audit.viewtask.view_task", name = "view_task"),
    #url(r"^audit/todotask", "ugc.audit.todotask.todo_task", name = "todo_task"),
    
)
