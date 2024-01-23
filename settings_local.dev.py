import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Add allowed hosts
ALLOWED_HOSTS = []

ADMINS = ()

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'INSERTSECRETKEYHERE'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

LOGIN_URL = '/manager/login/' # Modify for subdirectories
LOGOUT_URL = '/manager/logout/' # Modify for subdirectories
LOGIN_REDIRECT_URL = '/' # Modify for subdirectories
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static") # Comment out when using locally
STATICFILES_DIRS = [
    # Add static root path when debugging locally
    os.path.join(BASE_DIR, "static")
]

# Modify these values if hosting under subdirectory
FORCE_SCRIPT_NAME = '/'
CSRF_COOKIE_PATH = '/'
CSRF_COOKIE_HTTPONLY = False # Should be set to true in production environments
CSRF_COOKIE_SECURE = False # Should be set to true in production environments
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# NET Domain LDAP CONFIG
LDAP_NET_HOST = 'ldaps://you.ldap.com'
LDAP_NET_BASE_DN = 'cn=Users,dc=you,dc=ldap,dc=com'
LDAP_NET_USER_SUFFIX = '@you.ldap.com'
LDAP_NET_ATTR_MAP = { # LDAP Object -> User Object
    'givenName': 'first_name',
    'sn': 'sn',
    'mail': 'email'
}
LDAP_NET_SEARCH_USER = ''
LDAP_NET_SEARCH_PASS = ''
LDAP_NET_SEARCH_SIZELIMIT = 5

# Remote Menus

# JSON of Main Site Menu
REMOTE_MENU_HEADER = 'https://www.ucf.edu/wp-json/ucf-rest-menus/v1/menus/23/'
# JSON of Main Site Footer Menu
REMOTE_MENU_FOOTER = 'https://www.ucf.edu/wp-json/ucf-rest-menus/v1/menus/24/'

# Constants for Semesters
SPRING_MONTH_START = 1
SPRING_MONTH_END = 5
SUMMER_MONTH_START = 5
SUMMER_MONTH_END = 7
FALL_MONTH_START = 8
FALL_MONTH_END = 12

GTM_ID = ''

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'filters': {
        'require_debug_true': {
            '()': 'logs.RequiredDebugTrue',
        },
        'require_debug_false': {
            '()': 'logs.RequiredDebugFalse',
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
            'filename': os.path.join(BASE_DIR,'logs', 'application.log'),
            'formatter': 'concise',
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
            'handlers': ['discard'],
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
