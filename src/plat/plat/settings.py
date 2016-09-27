#!/usr/bin/python
# -*- coding:utf-8 -*-
# Django settings for plat project.

import os
import time

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'ch_old',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': 'root',
        'PASSWORD': 'funshion',
        'HOST': '192.168.177.3',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '3306',                      # Set to empty string for default.
    }
}

DATABASES_2 = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'xv',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': 'root',
        'PASSWORD': 'funshion',
        'HOST': '192.168.177.3',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '3306',                      # Set to empty string for default.
    }
}

DATABASES_3 = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'xvsync',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': 'root',
        'PASSWORD': 'funshion',
        'HOST': '192.168.177.3',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '3306',                      # Set to empty string for default.
    }
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Asia/Shanghai'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'zh_CN'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = False

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(BASE_DIR, 'static'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '522#$0jl1i+lu!$81k9i)xd09r5xr1e$aaa*3(p+bojd86ggka'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'pagination.middleware.PaginationMiddleware',
)

ROOT_URLCONF = 'plat.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'plat.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(BASE_DIR, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    'django.contrib.admindocs',
    'subscribe',
    'video_house',
    'pagination',
    'blacklist',
    'repost',
    'xvsync',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {#日志打印的格式
        'standard': {
            'format': '%(asctime)s [%(levelname)s] [%(funcName)s,%(lineno)s] - %(message)s'
        },
    },
#     'filters': {
#         'require_debug_false': {
#             '()': 'django.utils.log.RequireDebugFalse'
#         }
#     },
    'filters':{},
    'handlers': {#定义具体日志的处理方式，可以定义很多种
        'mail_admins': {
            'level': 'ERROR',
            #'filters': ['require_debug_false'],
            'filters':'',
            'class': 'django.utils.log.AdminEmailHandler',
             'formatter':'standard',
        },
        'default': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            #'filename': './log/%s'%time.strftime('%Y-%m-%d', time.gmtime()),
            'filename': './log/log.txt',
            #'maxBytes': 1024*1024*5, # 5 MB
            #'backupCount': 5,
            'formatter':'standard',
        },
        'console':{#打印到控制台方式
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        },
        'my_handler': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename':'./log/log.txt',
            'formatter':'standard',
        },
    },
    'loggers': {#配置用哪几种 handlers 来处理日志
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
#          'django': {#注释掉，在日志文件中就不会打印SQL语句了；否则就会打印SQL语句
#             'handlers': ['default'],
#             'level': 'DEBUG',
#             'propagate': False
#         },
        'my':{
            'handlers': ['my_handler'],
            'level': 'INFO',
            'propagate': False
        },
    }
}

LOGIN_REDIRECT_URL = "/main/"

TEMPLATE_CONTEXT_PROCESSORS = (  
#         "django.core.context_processors.auth",  
        "django.core.context_processors.debug",  
        "django.core.context_processors.i18n",  
        "django.core.context_processors.media",  
        "django.core.context_processors.request",
        "django.contrib.auth.context_processors.auth"
    )  

DATA_SERVER_IP = '192.168.16.156'
DATA_SERVER_PORT = '9888'

FLASHGET_SERVER_IP = '192.168.16.156'
FLASHGET_SERVER_PORT = '8090'
FLASHGET_GET_URL = '/get_url'

UPLOAD_SERVER_IP = '192.168.16.156'
UPLOAD_SERVER_PORT = '80'

PROXY_SERVER = '218.6.13.242:9437'

SCRAPYD_COMMAND = 'curl http://localhost:6800/schedule.json -d project=crawler -d spider=%s '

POSTERS_PATH = 'http://192.168.177.3:9537/img/'

