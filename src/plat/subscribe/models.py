# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals

from django.db import models

class Crawler(models.Model):
    spider_id = models.IntegerField(primary_key=True)
    spider_name = models.CharField(max_length=32L, blank=True)
    class Meta:
        db_table = 'crawler'

class Episode(models.Model):
#     id = models.BigIntegerField(unique=True)
    video_id = models.IntegerField(null=True, blank=True)
    show_id = models.CharField(max_length=32L, unique=True, blank=True)
    owner_show_id = models.CharField(max_length=32L, blank=True)
    title = models.CharField(max_length=256L, blank=True)
    category = models.CharField(max_length=64L, blank=True)
    tag = models.CharField(max_length=256L, blank=True)
    played = models.BigIntegerField(null=True, blank=True)
    upload_time = models.DateTimeField(null=True, blank=True)
    create_time = models.DateTimeField(null=True, blank=True)
    update_time = models.DateTimeField(null=True, blank=True)
    spider = models.ForeignKey(Crawler, null=True, blank=True)
    url = models.CharField(max_length=256L, blank=True)
    site = models.ForeignKey('Site', null=True, blank=True)
    thumb_url = models.CharField(max_length=256L, blank=True)
    description = models.TextField(blank=True)
    class Meta:
        db_table = 'episode'
'''
class Keyword(models.Model):
#     id = models.IntegerField(primary_key=True)
    keyword = models.CharField(max_length=64L, blank=True)
    type = models.CharField(max_length=8L, blank=True)
    user = models.CharField(max_length=32L, blank=True)
    site = models.ForeignKey('Site', null=True, blank=True, to_field='site_id')
    class Meta:
        db_table = 'keyword'
'''        
class Keyword(models.Model):
    id = models.IntegerField(primary_key=True)
    keyword = models.CharField(max_length=64L, blank=True)
    type = models.CharField(max_length=8L, blank=True)
    user = models.CharField(max_length=32L, blank=True)
    site = models.ForeignKey('Site', null=True, blank=True)
    ext_cat_id = models.CharField(max_length=8L, blank=True)
    class Meta:
        db_table = 'keyword'

class Ordered(models.Model):
    show = models.ForeignKey('Owner', unique=True, primary_key=True, to_field='show_id')
    user = models.CharField(max_length=32L, blank=True)
    ctime = models.DateTimeField(null=True, blank=True)
    site_id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = 'ordered'

class Owner(models.Model):
    id = models.IntegerField(unique=True, primary_key=True)
    owner_id = models.IntegerField(null=True, blank=True)
    show_id = models.CharField(max_length=32L, unique=True, blank=True)
    user_name = models.CharField(max_length=128L, blank=True)
    intro = models.TextField(blank=True)
    played = models.BigIntegerField(null=True, blank=True)
    fans = models.IntegerField(null=True, blank=True)
    vcount = models.IntegerField(null=True, blank=True)
    pcount = models.IntegerField(null=True, blank=True)
    create_time = models.DateTimeField(null=True, blank=True)
    update_time = models.DateTimeField(null=True, blank=True)
    spider = models.ForeignKey(Crawler, null=True, blank=True)
    aka = models.CharField(max_length=32L, blank=True)
    url = models.CharField(max_length=256L, blank=True)
    site = models.ForeignKey('Site', null=True, blank=True)
    class Meta:
        db_table = 'owner'

class Site(models.Model):
    site_id = models.IntegerField(primary_key=True)
    site_name = models.CharField(max_length=32L, blank=True)
    site_code = models.CharField(max_length=32L, blank=True)
    class Meta:
        db_table = 'site'

class Task(models.Model):
    task_id = models.IntegerField(primary_key=True)
    data_count = models.IntegerField(null=True, blank=True)
    begin_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = 'task'

class Page(models.Model):
#     id = models.IntegerField(primary_key=True)
    url = models.CharField(max_length=1024L, blank=True)
    ctime = models.CharField(max_length=8L, blank=True)
    user = models.CharField(max_length=32L, blank=True)
    site = models.ForeignKey('Site', null=True, blank=True, to_field='site_id')
    class Meta:
        db_table = 'page'
        
class Door(models.Model):
    class Meta:
        app_label = "subscribe"
        permissions = (
                       ("subs_youtube","Can_subs_youtube"),
                       ("unsubs_youtube","Can_unsubs_youtube"),
                       ("view_youtube","Can_view_youtube"),
                       ("subs_youku","Can_subs_youku"),
                       ("unsubs_youku","Can_unsubs_youku"),
                       ("view_youku","Can_view_youku"),
                       ("submit_video","Can_submit_video"),
        )
        managed=False
        
class ChannelExclude(models.Model):
    id = models.IntegerField(primary_key=True)
    show_id = models.CharField(max_length=32L, unique=True, blank=True)
    user_name = models.CharField(max_length=128L, blank=True)
    url = models.CharField(max_length=256L, blank=True)
    class Meta:
        db_table = 'channel_exclude'

class CatExclude(models.Model):
    id = models.IntegerField(primary_key=True)
    cat_name = models.CharField(max_length=64L, blank=True)
    class Meta:
        db_table = 'cat_exclude'

class CatList(models.Model):
    id = models.IntegerField(primary_key=True)
    cat_name = models.CharField(max_length=64L, blank=True)
    url = models.CharField(max_length=256L, blank=True)
    site = models.ForeignKey('Site', null=True, blank=True)
    class Meta:
        db_table = 'cat_list'
        
class CatListEpisode(models.Model):
    cat_id = models.IntegerField()
    show_id = models.CharField(max_length=32L)
    class Meta:
        db_table = 'cat_list_episode'
        
class Subject(models.Model):
    id = models.IntegerField(primary_key=True)
    subject_name = models.CharField(max_length=128L, blank=True)
    cat_name = models.CharField(max_length=64L, blank=True)
    url = models.CharField(max_length=256L, blank=True)
    site = models.ForeignKey(Site)
    class Meta:
        db_table = 'subject'

class SubjectEpisode(models.Model):
    subject_id = models.IntegerField()
    show_id = models.CharField(max_length=32L)
    class Meta:
        db_table = 'subject_episode'
        
class Blacklist(models.Model):
    id = models.IntegerField(primary_key=True)
    word = models.CharField(max_length=64L, blank=True)
    type = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = 'blacklist'
        

        