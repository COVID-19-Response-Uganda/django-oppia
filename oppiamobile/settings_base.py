"""
Django settings for OppiaMobile project.

Generated by 'django-admin startproject' using Django 1.11.11.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""
import os

from django.utils.translation import gettext_lazy as _

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'uzekt30thl4&hw)p@c#ht=b8mn!3l080kmnuk7ez+g5l%lb*p9'

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT_DIR = os.path.abspath(os.path.join(BASE_DIR, os.pardir))

ALLOWED_HOSTS = []
DEBUG = True

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'oppia.middleware.LoginRequiredMiddleware',

]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.i18n',
                'oppia.context_processors.get_points',
                'oppia.context_processors.get_version',
                'oppia.context_processors.get_settings',
                'oppia.context_processors.add_dashboard_access_log'
            ],
            'debug': True,
        },
    },
]

INSTALLED_APPS = [
    'activitylog',
    'av',
    'datarecovery',
    'gamification',
    'helpers',
    'integrations',
    'oppia',
    'profile',
    'quiz',
    'reports',
    'serverregistration',
    'settings',
    'summary',
    'viz',

    'tastypie',
    'crispy_forms',
    'sass_processor',
    'sorl.thumbnail',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework'
]

# Logging (automated error emails)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

TIME_ZONE = 'UTC'
USE_TZ = True
SITE_ID = 1

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(ROOT_DIR, 'static')
MEDIA_ROOT = os.path.join(ROOT_DIR, 'media')
ADMIN_MEDIA_PREFIX = '/static/admin/'

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'sass_processor.finders.CssFinder',
]

ROOT_URLCONF = 'oppiamobile.urls'
MEDIA_URL = '/media/'
STATIC_URL = '/static/'


# Email
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = '/tmp/'
SERVER_EMAIL = 'adming@email.org'


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/
LANGUAGE_CODE = 'en-GB'
USE_I18N = True
USE_L10N = True

LOCALE_PATHS = [
    os.path.join(BASE_DIR, "oppia", "locale")
]

LANGUAGES = [('en', _('English'))]

CRISPY_TEMPLATE_PACK = 'bootstrap4'

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# Login and logout settings
# https://docs.djangoproject.com/en/1.11/ref/settings/#login-redirect-url
LOGIN_URL = '/profile/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
# Exempt URLs (used by LoginRequiredMiddleware)
LOGIN_EXEMPT_URLS = (
    r'^server/$',
    r'^profile/login/$',
    r'^profile/register/',
    r'^profile/reset/',
    r'^profile/setlang/$',
    r'^profile/delete/complete/$',
    r'^$',
    r'^about/$',
    r'^terms/$',
    r'^api/',  # allow any URL under api/* - auth handled by api_key
    r'^media/temp/',
    r'^media/uploaded/',
    r'^api/activitylog/',
    r'^view/$',
    r'^accounts/password_reset/',
    r'^accounts/reset/',
    r'^certificate/validate/'
)

# OppiaMobile Settings
COURSE_UPLOAD_DIR = os.path.join(ROOT_DIR, 'upload')

# External storage
OPPIA_EXTERNAL_STORAGE = False

OPPIA_EXTERNAL_STORAGE_MEDIA_ROOT = None  # only used if OPPIA_EXTERNAL_STORAGE is set to True
OPPIA_EXTERNAL_STORAGE_MEDIA_URL = None  # only used if OPPIA_EXTERNAL_STORAGE is set to True

OPPIA_EXTERNAL_STORAGE_COURSE_ROOT = None  # only used if OPPIA_EXTERNAL_STORAGE is set to True
OPPIA_EXTERNAL_STORAGE_COURSE_URL = None  # only used if OPPIA_EXTERNAL_STORAGE is set to True

OPPIA_METADATA = {
    'NETWORK': False,
    'DEVICE_ID': False,
    'SIM_SERIAL': False,
    'WIFI_ON': True,
    'NETWORK_CONNECTED': True,
    'BATTERY_LEVEL': False,
}

# Sublist of oppia.models.main.CourseStatus choices. Only the CourseStatus IDs in this list will appear when choosing
# a course status.
OPPIA_AVAILABLE_COURSE_STATUSES = ['live', 'archived', 'draft', 'new_downloads_disabled', 'read_only']

# turns on/off ability for users to self register
OPPIA_ALLOW_SELF_REGISTRATION = True
OPPIA_ALLOW_PROFILE_EDITING = True
OPPIA_SHOW_GRAVATARS = True

# determines if the points system is enabled
OPPIA_POINTS_ENABLED = True

# determines if the badges system is enabled
OPPIA_BADGES_ENABLED = True

BADGE_AWARDING_METHOD = 'all_activities'

OPPIA_GOOGLE_ANALYTICS_ENABLED = False
OPPIA_GOOGLE_ANALYTICS_CODE = 'YOUR_GOOGLE_ANALYTICS_CODE'
OPPIA_GOOGLE_ANALYTICS_DOMAIN = 'YOUR_DOMAIN'

OPPIA_MAX_UPLOAD_SIZE = 5242880  # max course file upload size - in bytes

OPPIA_VIDEO_FILE_TYPES = ("video/m4v", "video/mp4", "video/3gp", "video/3gpp")
OPPIA_AUDIO_FILE_TYPES = ("audio/mpeg", "audio/amr", "audio/mp3")
OPPIA_MEDIA_FILE_TYPES = OPPIA_VIDEO_FILE_TYPES + OPPIA_AUDIO_FILE_TYPES

OPPIA_UPLOAD_TRACKER_FILE_TYPES = [("application/json")]

# Android app PackageId - for Google Play link and opening activities
# from digest
OPPIA_ANDROID_DEFAULT_PACKAGEID = 'org.digitalcampus.mobile.learning'
OPPIA_ANDROID_PACKAGEID = 'org.digitalcampus.mobile.learning'

# if the app is not on Google Play, we rely on the core version for store
# links
OPPIA_ANDROID_ON_GOOGLE_PLAY = True

MEDIA_PROCESSOR_PROGRAM = "ffprobe"
MEDIA_PROCESSOR_PROGRAM_PARAMS = ""

# for API v1 and v2
API_LIMIT_PER_PAGE = 0

# for API v3
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ]
}
