# Django settings for rpi_csdt_community project.
import os

PROJECT_ROOT = os.path.join(*os.path.realpath(__file__).split(os.sep)[:-2])

if os.path.splitdrive(PROJECT_ROOT)[0] != '':
    PROJECT_ROOT = os.path.splitdrive(PROJECT_ROOT)[0] + os.sep + os.path.splitdrive(PROJECT_ROOT)[1]
else:
    PROJECT_ROOT = os.path.join('/', PROJECT_ROOT)


DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': PROJECT_ROOT + '/database.sqlite3',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': '',
        'PASSWORD': '',
        'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
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
MEDIA_ROOT = PROJECT_ROOT + '/media/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = PROJECT_ROOT + '/collected_static/'

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    PROJECT_ROOT + '/static/',
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
    'pipeline.finders.PipelineFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'n)ntn6k*y6tt5zd5m!0$&qd$y_*rpv5m87-ld4f7suj8%shd^4'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    # 'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',

    'likes.middleware.SecretBallotUserIpUseragentMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'rpi_csdt_community.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'rpi_csdt_community.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    PROJECT_ROOT + '/templates/',
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
    'taggit',
    'taggit_templatetags',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    # ... include the providers you want to enable:
    #'allauth.socialaccount.providers.amazon',
    #'allauth.socialaccount.providers.angellist',
    #'allauth.socialaccount.providers.bitbucket',
    #'allauth.socialaccount.providers.bitly',
    #'allauth.socialaccount.providers.coinbase',
    #'allauth.socialaccount.providers.dropbox',
    'allauth.socialaccount.providers.facebook',
    #'allauth.socialaccount.providers.flickr',
    'allauth.socialaccount.providers.github',
    #'allauth.socialaccount.providers.feedly',
    #'allauth.socialaccount.providers.google',
    #'allauth.socialaccount.providers.hubic',
    #'allauth.socialaccount.providers.instagram',
    #'allauth.socialaccount.providers.linkedin',
    #'allauth.socialaccount.providers.linkedin_oauth2',
    #'allauth.socialaccount.providers.openid',
    #'allauth.socialaccount.providers.persona',
    #'allauth.socialaccount.providers.soundcloud',
    #'allauth.socialaccount.providers.stackexchange',
    #'allauth.socialaccount.providers.tumblr',
    #'allauth.socialaccount.providers.twitch',
    'allauth.socialaccount.providers.twitter',
    #'allauth.socialaccount.providers.vimeo',
    #'allauth.socialaccount.providers.vk',
    #'allauth.socialaccount.providers.weibo',
    #'allauth.socialaccount.providers.xing',

    'captcha',
    'django_extensions',
    'project_share',
    'rpi_csdt_community',
    'twitter_bootstrap',
    'pipeline',
    'jquery',


#    'filer',
#    'easy_thumbnails',

    'attachments',

    'sorl.thumbnail',

    'extra_views',

    'secretballot',
    'likes',

    'django.contrib.comments',
    'django_comments_xtd',
    'django_markup',
#    'pybb',
#    'south',
    'rest_framework',
    'django_teams',
)

CAPTCHA_CHALLENGE_FUNCT = 'captcha.helpers.math_challenge'
CAPTCHA_NOISE_FUNCTIONS = ()

COMMENTS_APP = "django_comments_xtd"
COMMENTS_XTD_MAX_THREAD_LEVEL = 8
COMMENTS_XTD_CONFIRM_EMAIL = True

from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP

TEMPLATE_CONTEXT_PROCESSORS = TCP + (
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
    'allauth.account.context_processors.account',
    'allauth.socialaccount.context_processors.socialaccount',
)

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
)

AUTH_USER_MODEL = 'project_share.ExtendedUser'

# This should probably be defined in local_settings.py, since it is external
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

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

SOUTH_TESTS_MIGRATE = False
SOUTH_MIGRATION_MODULES = {
    'taggit': 'taggit.south_migrations',
}

THUMBNAIL_DEBUG = False

LOGIN_REDIRECT_URL = '/'

STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'

# Stuff related to the asset pipline
PIPELINE_CSS = {
    'bootstrap': {
        'source_filenames': (
            'twitter_bootstrap/less/bootstrap.less',
        ),
        'output_filename': 'css/b.css',
        'extra_context': {
            'media': 'screen,projection',
        },
    },
    'base_style': {
        'source_filenames': (
            'less/style.less',
        ),
        'output_filename': 'css/s.css',
        'extra_context': {
            'media': 'screen,projection',
        },
    }
}

PIPELINE_JS = {
    'bootstrap': {
        'source_filenames': (
          'twitter_bootstrap/js/transition.js',
          'twitter_bootstrap/js/modal.js',
          'twitter_bootstrap/js/dropdown.js',
          'twitter_bootstrap/js/scrollspy.js',
          'twitter_bootstrap/js/tab.js',
          'twitter_bootstrap/js/tooltip.js',
          'twitter_bootstrap/js/popover.js',
          'twitter_bootstrap/js/alert.js',
          'twitter_bootstrap/js/button.js',
          'twitter_bootstrap/js/collapse.js',
          'twitter_bootstrap/js/carousel.js',
          'twitter_bootstrap/js/affix.js',
        ),
        'output_filename': 'js/b.js',
    },
    'jquery': {
        'source_filenames': {
            'js/jquery.js',
        },
        'output_filename': 'js/j.js',
    },
}

PIPELINE_COMPILERS = (
    'pipeline.compilers.less.LessCompiler',
)


# Track where my LESS things live
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

my_app_less = os.path.join(BASE_DIR, 'my_app', 'static', 'less')

# For apps outside of your project, it's simpler to import them to find their root folders
import twitter_bootstrap
bootstrap_less = os.path.join(os.path.dirname(twitter_bootstrap.__file__), 'static', 'twitter_bootstrap', 'less')

PIPELINE_LESS_ARGUMENTS = u'--include-path={}'.format(os.pathsep.join([bootstrap_less, my_app_less]))

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

try:
    from local_settings import *
except:
    pass
