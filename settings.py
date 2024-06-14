"""
Django settings for src project.

Generated by 'django-admin startproject' using Django 1.10.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import environ
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

env = environ.FileAwareEnv()

environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

DEBUG = env('DEBUG', bool, default=True)

#ALLOWED_HOSTS = env('ALLOWED_HOSTS', list, default=[])

ALLOWED_HOSTS = [*]

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY', str, default='INSERTSECRETKEYHERE')

DATABASES = {
    'default': env.db(
        'DATABASE_URL',
        default=f'sqlite:////{os.path.join(BASE_DIR, "db.sqlite3")}'
    )
}

LOGIN_URL = env('LOGIN_URL', str, default='/manager/login/') # Modify for subdirectories
LOGOUT_URL = env('LOGOUT_URL', str, default='/manager/logout/') # Modify for subdirectories
LOGIN_REDIRECT_URL = env('LOGIN_REDIRECT_URL', str, default='/') # Modify for subdirectories
STATIC_URL = env('STATIC_URL', str, default='/static/')

static_root = env('STATIC_ROOT', str, default=None)

if static_root is not None:
    STATIC_ROOT = os.path.join(BASE_DIR, static_root)

STATICFILES_DIRS = default=[]

staticfile_dir = env('STATICFILES_DIR', str, default=None)
if staticfile_dir is not None:
    STATICFILES_DIRS.append(
        os.path.join(BASE_DIR, staticfile_dir)
    )

# Modify these values if hosting under subdirectory
FORCE_SCRIPT_NAME = env('FORCE_SCRIPT_NAME', str, default='/')
CSRF_COOKIE_PATH = env('CSRF_COOKIE_PATH', str, default='/')
CSRF_COOKIE_HTTPONLY = env('CSRF_COOKIE_HTTPONLY', bool, default=False) # Should be set to true in production environments
CSRF_COOKIE_SECURE = env('CSRF_COOKIE_SECURE', bool, default=False) # Should be set to true in production environments
CSRF_TRUSTED_ORIGINS = env('CSRF_TRUSTED_ORIGINS', list, default=['http://localhost:8000'])
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# NET Domain LDAP CONFIG
LDAP_NET_HOST = env('LDAP_NET_HOST', str, default='ldaps://you.ldap.com')
LDAP_NET_BASE_DN = env('LDAP_NET_BASE_DN', str, default='cn=Users,dc=you,dc=ldap,dc=com')
LDAP_NET_USER_SUFFIX = env('LDAP_NET_USER_SUFFIX', str, default='@you.ldap.com')
LDAP_NET_ATTR_MAP = { # LDAP Object -> User Object
    'givenName': 'first_name',
    'sn': 'sn',
    'mail': 'email'
}
LDAP_NET_SEARCH_USER = env('LDAP_NET_SEARCH_USER', str, default='')
LDAP_NET_SEARCH_PASS = env('LDAP_NET_SEARCH_PASS', str, default='')
LDAP_NET_SEARCH_SIZELIMIT = env('LDAP_NET_SEARCH_SIZELIMIT', int, default=5)

# JSON of Main Site Menu
REMOTE_MENU_HEADER = env('REMOTE_MENU_HEADER', str, default='https://www.ucf.edu/wp-json/ucf-rest-menus/v1/menus/23/')
# JSON of Main Site Footer Menu
REMOTE_MENU_FOOTER = env('REMOTE_MENU_HEADER', str, default='https://www.ucf.edu/wp-json/ucf-rest-menus/v1/menus/24/')

# Constants for Semesters
SPRING_MONTH_START = env('SPRING_MONTH_START', int, default=1)
SPRING_MONTH_END = env('SPRING_MONTH_END', int, default=5)
SUMMER_MONTH_START = env('SUMMER_MONTH_START', int, default=5)
SUMMER_MONTH_END = env('SUMMER_MONTH_END', int, default=7)
FALL_MONTH_START = env('FALL_MONTH_START', int, default=8)
FALL_MONTH_END = env('FALL_MONTH_END', int, default=12)

GTM_ID = env('GTM_ID', str, default='')

DAYS_UNTIL_EXPIRED = env('DAYS_UNTIL_EXPIRED', int, default=90)

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sitemaps',
    'django.contrib.staticfiles',
    'announcements',
    'taggit',
    'widget_tweaks',
    'rest_framework',
    'rest_framework.authtoken',
    'markdown',
    'bleach',
    'django_filters',
    'drf_dynamic_fields'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'announcements.auth.Backend',
)

ROOT_URLCONF = 'urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            'templates'
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'announcements.context_processors.seo.seo_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'wsgi.application'


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Rest Framework Settings
REST_FRAMEWORK = {
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    )
}

# Taggit settings
TAGGIT_CASE_INSENSITIVE = True

# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        }
    },
    'formatters': {
        'talkative': {
            'format': '[%(asctime)s] %(levelname)s:%(module)s %(funcName)s %(lineno)d %(message)s'
        },
        'concise': {
            'format': '%(levelname)s: %(message)s (%(asctime)s)'
        }
    },
    'handlers': {
        'discard': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'talkative',
            'filters': ['require_debug_true']
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'application.log'),
            'formatter': 'talkative',
            'filters': ['require_debug_false']
        }
    },
    'loggers': {
        'core': {
            'handlers': ['console', 'file'],
            'propogate': True,
            'level': 'WARNING'
        },
        'django': {
            'handlers': ['console', 'file'],
            'propogate': True,
            'level': 'WARNING'
        },
        'events': {
            'handlers': ['console', 'file'],
            'propogate': True,
            'level': 'WARNING'
        },
        'profiles': {
            'handlers': ['console', 'file'],
            'propogate': True,
            'level': 'WARNING'
        },
        'util': {
            'handlers': ['console', 'file'],
            'level': 'WARNING'
        }
    }
}
