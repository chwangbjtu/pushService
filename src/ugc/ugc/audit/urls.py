from django.conf.urls import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       url(r"^$","ugc.audit.views.home_page",name = "homepage"),
                       url(r"^applytask", "ugc.audit.apply_task.apply_task", name = "applytask"),
                       url(r"^navtree","ugc.audit.views.nav_tree"),
                       url(r"^welcome","ugc.audit.views.welcome"),
                       url(r"^showvideo","ugc.audit.showtask.show_task"),
                       url(r"^nextvideo","ugc.audit.audit_video_bk.nav_to_next"),
                       url(r"^playvideo","ugc.audit.play_video.play_video"),
                       url(r"^onauditvideo","ugc.audit.audit_video_bk.audit_video"),
                       url(r"^user_all_video","ugc.audit.views.user_all_video", name = "user_all_video"),
                       url(r"^distribute_video_count","ugc.audit.views.distribute_video_count", name = "distribute_video_count"),
                       url(r"^distribute_video_search","ugc.audit.views.distribute_video_search", name = "distribute_video_search"),
                       url(r"^user_pending_video","ugc.audit.views.user_pending_video", name = "user_pending_video"),
                       url(r"^user_passed_video","ugc.audit.views.user_passed_video", name = "user_passed_video"),
                       url(r"^user_failure_video","ugc.audit.views.user_failure_video", name = "user_failure_video"),
                       url(r"^admin_all_video","ugc.audit.views.admin_all_video", name = "admin_all_video"),
                       url(r"^admin_pending_video","ugc.audit.views.admin_pending_video", name = "admin_pending_video"),
                       url(r"^admin_passed_video","ugc.audit.views.admin_passed_video", name = "admin_passed_video"),
                       url(r"^admin_failure_video","ugc.audit.views.admin_failure_video", name = "admin_failure_video"),
                       url(r"^unreg","ugc.audit.views.unreg", name = "unreg"),
                       url(r"^user_count","ugc.audit.views.user_count", name = "user_count"),
                       url(r"^jstest","ugc.audit.views.jstest", name = "jstest"),
                       url(r"^redirect_to_msvideo","ugc.audit.views.play_msvideo",)
                       )
