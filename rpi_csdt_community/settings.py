"""Django settings for rpi_csdt_community project."""
import os

import twitter_bootstrap

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))

DEBUG = True
if not DEBUG:
    GOOGLE_ANALYTICS_PROPERTY_ID = 'UA-77115650-1'
    GOOGLE_ANALYTICS_DOMAIN = 'rpi.edu'

# Override this setting local_settings.py to enable the GIS app
ENABLE_GIS = False

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS
if 'TRAVIS' in os.environ:
    DATABASES = {
        'default': {
            'ENGINE':   'django.db.backends.postgresql_psycopg2',
            'NAME':     'travisci',
            'USER':     'postgres',
            'PASSWORD': '',
            'HOST':     'localhost',
            'PORT':     '',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'rpi_csdt_community',
            'USER': 'postgres',
            'PASSWORD': 'postgres',
            'HOST': 'localhost',
        }
    }

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/New_York'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

LANGUAGES = [
    ('en-us', 'English'),
]

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media/')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'collected_static/')
STATIC_WEBSITE_ROOT = os.path.join(PROJECT_ROOT, 'static/website/www')

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_ROOT, 'static/'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
    'compressor.finders.CompressorFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'n)ntn6k*y6tt5zd5m!0$&qd$y_*rpv5m87-ld4f7suj8%shd^4'

MIDDLEWARE = [
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
    'cms.middleware.language.LanguageCookieMiddleware',
]

ROOT_URLCONF = 'rpi_csdt_community.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'rpi_csdt_community.wsgi.application'

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
    'django_comments',
    'taggit',
    'taggit_templatetags2',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    # ... include the providers you want to enable:
    # 'allauth.socialaccount.providers.amazon',
    # 'allauth.socialaccount.providers.angellist',
    # 'allauth.socialaccount.providers.bitbucket',
    # 'allauth.socialaccount.providers.bitly',
    # 'allauth.socialaccount.providers.coinbase',
    # 'allauth.socialaccount.providers.dropbox',
    'allauth.socialaccount.providers.facebook',
    # 'allauth.socialaccount.providers.flickr',
    'allauth.socialaccount.providers.github',
    # 'allauth.socialaccount.providers.feedly',
    # 'allauth.socialaccount.providers.google',
    # 'allauth.socialaccount.providers.hubic',
    # 'allauth.socialaccount.providers.instagram',
    # 'allauth.socialaccount.providers.linkedin',
    # 'allauth.socialaccount.providers.linkedin_oauth2',
    # 'allauth.socialaccount.providers.openid',
    # 'allauth.socialaccount.providers.persona',
    # 'allauth.socialaccount.providers.soundcloud',
    # 'allauth.socialaccount.providers.stackexchange',
    # 'allauth.socialaccount.providers.tumblr',
    # 'allauth.socialaccount.providers.twitch',
    'allauth.socialaccount.providers.twitter',
    # 'allauth.socialaccount.providers.vimeo',
    # 'allauth.socialaccount.providers.vk',
    # 'allauth.socialaccount.providers.weibo',
    # 'allauth.socialaccount.providers.xing',

    'captcha',
    'django_extensions',
    'project_share',
    'rpi_csdt_community',
    'twitter_bootstrap',
    'jquery',


    'easy_thumbnails',
    'filer',

    'attachments',

    'extra_views',

    'django_markup',
    'rest_framework',
    'django_teams',
    'django_comments_xtd',

    # Django CMS
    'treebeard',
    'djangocms_text_ckeditor',  # note this needs to be above the 'cms' entry
    'cms',  # django CMS itself
    'mptt',  # utilities for implementing a tree
    'menus',  # helper for model independent hierarchical website navigation
    'sekizai',  # for javascript and css management
    # for the admin skin. You **must** add 'djangocms_admin_style' in the list **before** 'django.contrib.admin'.
    'djangocms_admin_style',
    'djangocms_file',
    # 'djangocms_flash',
    # 'djangocms_googlemap',
    # 'djangocms_inherit',
    'djangocms_picture',
    # 'djangocms_teaser',
    # 'djangocms_video',
    'djangocms_link',
    # 'djangocms_snippet',
    'cms_bootstrap_templates',
    'compressor',
    'analytical',
    'blogposts',
    'comments',
    'markdown_deux',
    'crispy_forms',
    'guides',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(PROJECT_ROOT, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'sekizai.context_processors.sekizai',
                'cms.context_processors.cms_settings'
            ],
        },
    },
]


AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
)

AUTH_USER_MODEL = 'project_share.ExtendedUser'
ACCOUNT_SIGNUP_FORM_CLASS = 'project_share.forms.ExtendedSignupForm'

CMS_TEMPLATES = (
    ('cms_bootstrap_templates/template_one_column.html', 'One columns'),
    ('cms_bootstrap_templates/template_two_column.html', 'Two columns'),
    ('cms_bootstrap_templates/template_three_column.html', 'Three columns'),
    ('cms_bootstrap_templates/template_header_two_column.html', 'Two columns with a header'),
    ('cms_bootstrap_templates/template_header_two_column_left.html', 'Two columns w/ header, large left'),
    ('cms_bootstrap_templates/template_header_two_column_right.html', 'Two columns w/ header, large right'),
)

CMS_SOFTROOT = True

REST_FRAMEWORK = {
    # Use hyperlinked styles by default.
    # Only used if the `serializer_class` attribute is not set on a view.
    'DEFAULT_MODEL_SERIALIZER_CLASS':
        'rest_framework.serializers.HyperlinkedModelSerializer',

    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
}

THUMBNAIL_DEBUG = False

THUMBNAIL_PROCESSORS = (
    'easy_thumbnails.processors.colorspace',
    'easy_thumbnails.processors.autocrop',
    # 'easy_thumbnails.processors.scale_and_crop',
    'filer.thumbnail_processors.scale_and_crop_with_subject_location',
    'easy_thumbnails.processors.filters',
)

TEXT_HTML_SANITIZE = False


LOGIN_REDIRECT_URL = '/'

# Track where my LESS things live
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

MY_LESS_APP = os.path.join(BASE_DIR, 'static', 'less')

# For apps outside of your project, it's simpler to import them to find their root folders
BOOTSTRAP_LESS = os.path.join(os.path.dirname(twitter_bootstrap.__file__), 'static', 'twitter_bootstrap', 'less')

COMPRESS_ENABLED = False
COMPRESS_LESSC_COMMAND = 'lessc --include-path={}'.format(os.pathsep.join([BOOTSTRAP_LESS, MY_LESS_APP]))
COMPRESS_LESSC_COMMAND += " {infile} {outfile}"

COMPRESS_PRECOMPILERS = (
    ('text/less', COMPRESS_LESSC_COMMAND),
    ('stylesheet/less', COMPRESS_LESSC_COMMAND),
)


# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
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

WARNING_MESSAGE = "<strong>You are currently looking at the development site!</strong> None of this is real!"

USE_CACHE = False

try:
    from local_settings import *  # noqa: F403
except:
    pass

if USE_CACHE:
    MIDDLEWARE += [
        'django.middleware.cache.UpdateCacheMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.cache.FetchFromCacheMiddleware',
    ]


if ENABLE_GIS:
    # Make sure the database is configured as postgres
    assert DATABASES['default']['ENGINE'] == 'django.contrib.gis.db.backends.postgis'
    INSTALLED_APPS += (
        'gis_csdt',
        'django.contrib.gis',
    )

    # Make sure a GOOGLE_API_KEY is defined
    try:
        GOOGLE_API_KEY  # noqa: F405
    except NameError:
        raise "To use GIS, you need to define a GOOGLE_API_KEY"
    try:
        CENSUS_API_KEY  # noqa: F405
    except NameError:
        raise "To use GIS, you need to define a CENSUS API KEY"
