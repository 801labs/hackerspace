# Django settings for hackerspace project.
import os

BASE_DIR = '/webapps/hackerspace/live/'
DEBUG = False
#DEBUG = True
TEMPLATE_DEBUG = DEBUG

EMAIL_HOST = '127.0.0.1'
EMAIL_PORT = 25


SESSION_COOKIE_AGE = 1800
#801LABS SANDBOX
BRAINTREE_ENVIRONMENT  = 'production'
#SANDBOX
#BRAINTREE_CLIENT_KEY = 'MIIBCgKCAQEAwhAB8YX3kovhUnH66FRW4hFyEmiiTEaErt+phwF4oT0Mle8lh4MdOlL82VqHE+CxqY+M9UGsVrx85LvQIiGojynrbNOnaEuGGDj5/nyd73qzroydqBCpSDSPHuEeSwl5D3kNh4bmz+02VoAJ93JUzop/+YcRtEhUN0+AEHX1tZVkx/drFU189UC2S5tBThJhKFAZcFng2a6w38Mn9ekhVptB2najJnR6okQ0vFeMGUcgIrspePZ47kGiiC8I4MBwERCp6b+QMk0Chn0Sxsh+MKufv7GCBFCvcczCLkUt/eoTnxPuXkUsy6bCpOp+rIep0HbDGgg6SU4GyYg3YrObTwIDAQAB'

#BRAINTREE_MERCHANT_ID   =   "nwryd3rpxj4xh4q8"
#BRAINTREE_PUBLIC_KEY    =   "fb8qtwp5w8wsysrb"
#BRAINTREE_PRIVATE_KEY   =   "your_password"


#PRODUCTION TRANSISTOR
#BRAINTREE_CLIENT_KEY = 'MIIBCgKCAQEA2EovHBDtUf27CAQivZh0cfLZ5hwMiDECY9clmeWN1jj7i2imSykRVdcAOK3r2yTvzi1QDi/Q8VwoXBUN6vG1/CXz60AtFJrSPN79vJZT8Mn2lOkPxF/UxhlDVgmrAwlYyKMd62INcgfY0XrUnBr+F7eP+IaNehKFU9VnqfNLRWyeKoUYJJawsL011/tCCAb8cXNhtEUIFtFooVw3KlqNqdfC8kW7DJ1CDDI35mW5l/uy0hFLPsFGyi0ZDsD23syUAEI/9Gu/aR6nvKV/9wNgOyUUiFCc+seBzVJmU8faw0xc9dNtexxhgJ62zbvXhH3Xw4TalHBNrc2ZtrWjO6+VnwIDAQAB'

#BRAINTREE_MERCHANT_ID   =   "b4b5bnw9g54crgzm"
#BRAINTREE_PUBLIC_KEY    =   "mp35y7nc3n9qgbwx"
#BRAINTREE_PRIVATE_KEY   =   "your_password"

#PRODUCTION 801Labs
BRAINTREE_CLIENT_KEY = 'MIIBCgKCAQEAvKQTaPJxQOxBobBtVitj2FP7CCO1XPSYsFYdPY1aHIYMWWc32mDQv0t3SbHmerzbqimeZafeW5ASR8BMiiBeF6Jqv5Hlnxi1w386fgiQnOPjTorwJ3lRwq8DHMxBXURCO5ph4MbNm4/bOOEZXNa+bkYk0ydP1TT/6fyMH6yC3T25Al2DDIQvcxjKBcMQtfwwtw9iw+Na+hfUYPzNd4QWAinkPDX0nsc52EgSOzzbLjvM++lpVQQggn6BkaOFFfB6xeQC+aSabP4hJZ3TT96vS4aFZ9fc4WB3b4WF8ivktHzojxGdxGCVFIZyAd3JTdJVlN96EUKnl56LUcggiEl+AQIDAQAB'

BRAINTREE_MERCHANT_ID   =   "yx6x5k8m3369zxjb"
BRAINTREE_PUBLIC_KEY    =   "tynqpqxwvv5ktdf3"
BRAINTREE_PRIVATE_KEY   =   "your_password"
 

RECAPTCHA_PUBLIC_KEY    = '6LdecOsSAAAAAJWW3_Nbn18gBT8vwONZpMTi4Atb'
RECAPTCHA_PRIVATE_KEY   = 'your_password'

RECAPTCHA_USE_SSL = True

ADMIN_MEDIA_PREFIX = '/static/admin/'

ADMINS = (
        ('Lance Buttars', 'nemus@grayhatlabs.com'),
        ('Danny Howerton','metacortex@dc801.org'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'hackerspace',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
    }
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['801labs.org','www.801labs.org','*']
AUTH_USER_MODEL = 'members.DC801User'

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Denver'

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
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = '//webapps/hackerspace/live/static/'
# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'o$e9*52dv!ey0f0!swupnxpxp$a2q@a&&h_*tg2jb=put4e(+e'

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
)

ROOT_URLCONF = 'hackerspace.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'hackerspace.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'members',
    'captcha',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
)

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'

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
