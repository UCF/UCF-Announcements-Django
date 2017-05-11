import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

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
LOGIN_URL = '/login/'
LOGOUT_URL = '/logout/'
LOGIN_REDIRECT_URL = '/'


# Modify these values if hosting under subdirectory
FORCE_SCRIPT_NAME = '/'
CSRF_COOKIE_PATH = '/'
CSRF_COOKIE_SECURE = False
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_X_FORWARDED_HOST = True
USE_X_FORWARDED_PORT = True
USE_X_FORWARDED_PROTO = True

LOGIN_URL = '/manager/login/'
LOGOUT_URL = '/manager/logout/'
STATIC_URL = '/static/'
# STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static")
]

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
REMOTE_MENU_HEADER = 'http://www.ucf.edu/wp-json/ucf-rest-menus/v1/menus/52/' # JSON of Main Site Menu
REMOTE_MENU_FOOTER = 'http://www.ucf.edu/wp-json/ucf-rest-menus/v1/menus/48/' # JSON of Main Site Footer Menu