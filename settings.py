# Django settings file for a project based on the playdoh template.

import os
import logging

from django.utils.functional import lazy

# Make file paths relative to settings.
ROOT = os.path.dirname(os.path.abspath(__file__))
path = lambda *a: os.path.join(ROOT, *a)

ROOT_PACKAGE = os.path.basename(ROOT)


DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = ()
MANAGERS = ADMINS

DATABASES = {}  # See settings_local.

# Site ID is used by Django's Sites framework.
SITE_ID = 1

## Logging
LOG_LEVEL = logging.DEBUG
HAS_SYSLOG = False
SYSLOG_TAG = "http_app_playdoh" # Change this after you fork.
LOGGING_CONFIG = None
LOGGING = {
    }

# CEF Logging
CEF_PRODUCT = 'Playdoh'
CEF_VENDOR = 'Mozilla'
CEF_VERSION = '0'
CEF_DEVICE_VERSION = '0'


#Bleach settings
TAGS = ('h1', 'h2', 'a', 'b', 'em', 'i', 'strong',
        'ol', 'ul', 'li', 'blockquote', 'p',
        'span', 'pre', 'code', 'img')

ALLOWED_ATTRIBUTES = {
    'a': ['href', 'title'],
    'img': ['src', 'alt', 'title'],
}

APP_NAME = 'Mozilla Ignite'
APP_URL = 'http://www.mozillaignite.org'

## Internationalization.

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Los_Angeles'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Gettext text domain
TEXT_DOMAIN = 'messages'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-US'

# Accepted locales
KNOWN_LANGUAGES = ('en-US',)

# List of RTL locales known to this project. Subset of LANGUAGES.
RTL_LANGUAGES = ()  # ('ar', 'fa', 'fa-IR', 'he')

LANGUAGE_URL_MAP = dict([(i.lower(), i) for i in KNOWN_LANGUAGES])

# Override Django's built-in with our native names
class LazyLangs(dict):
    def __new__(self):
        from product_details import product_details
        return dict([(lang.lower(), product_details.languages[lang]['native'])
                     for lang in KNOWN_LANGUAGES])

# Where to store product details etc.
PROD_DETAILS_DIR = path('lib/product_details_json')

LANGUAGES = lazy(LazyLangs, dict)()

# Paths that don't require a locale code in the URL.
SUPPORTED_NONLOCALES = ['media', 'push']


## Media and templates.

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = path('media/ignite')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/ignite/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/admin-media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = ''

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'session_csrf.context_processor',
    'django.contrib.messages.context_processors.messages',

    'commons.context_processors.i18n',
    'jingo_minify.helpers.build_ids',

    'topics.context_processors.topics',
    'django.core.context_processors.request',
    'innovate.context_processors.app_name',
    'ignite.context_processors.site_url'
)

TEMPLATE_DIRS = (
    path('templates'),
)

def JINJA_CONFIG():
    import jinja2
    from django.conf import settings
#    from caching.base import cache
    config = {'extensions': ['tower.template.i18n', 'jinja2.ext.do',
                             'jinja2.ext.with_', 'jinja2.ext.loopcontrols'],
              'finalize': lambda x: x if x is not None else ''}
#    if 'memcached' in cache.scheme and not settings.DEBUG:
        # We're passing the _cache object directly to jinja because
        # Django can't store binary directly; it enforces unicode on it.
        # Details: http://jinja.pocoo.org/2/documentation/api#bytecode-cache
        # and in the errors you get when you try it the other way.
#        bc = jinja2.MemcachedBytecodeCache(cache._cache,
#                                           "%sj2:" % settings.CACHE_PREFIX)
#        config['cache_size'] = -1 # Never clear the cache
#        config['bytecode_cache'] = bc
    return config

# Bundles is a dictionary of two dictionaries, css and js, which list css files
# and js files that can be bundled together by the minify app.
MINIFY_BUNDLES = {
    'css': {
        'ignite_devices' : (
            'css/normalise.css',
            'css/devices.css',
        ),
        'ignite_desktop' : (
            'css/desktop.css',
        ),
    },
    'js': {
        'ignite_core': (
            'js/common/ext/jquery-1.6.1.min.js',
            'js/common/ext/LAB.min.js',
            'js/common/core.js',
            'js/common/lacky.js',
        ),
    }
}

## Middlewares, apps, URL configs.

MIDDLEWARE_CLASSES = (
    'commons.middleware.LocaleURLMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'session_csrf.CsrfMiddleware',
    'commonware.middleware.FrameOptionsHeader',
    'ignite.middleware.ProfileMiddleware',
    'waffle.middleware.WaffleMiddleware',
)

ROOT_URLCONF = '%s.urls' % ROOT_PACKAGE

INSTALLED_APPS = (
    # Local apps
    'commons',  # Content common to most playdoh-based apps.
    'jingo_minify',
    'tower',  # for ./manage.py extract (L10n)
    'cronjobs',  # for ./manage.py cron * cmd line tasks

    # We need this so the jsi18n view will pick up our locale directory.
    ROOT_PACKAGE,

    # Third-party apps
    'commonware.response.cookies',
    #'djcelery',
    'django_nose',
    'django_extensions',

    # Django contrib apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django_sha2',  # Load after auth to monkey-patch it.

    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',

    # L10n
    'product_details',

    # Database migrations
    'south',

    # BrowserID support
    'django_browserid',

    # Tagging
    'taggit',

    # Feed subscription
    'django_push.subscriber',
    'feeds',
    # email queue
    #'django_mailer',

    # Feature flipping
    'waffle',
    'haystack',   # search

    # Ignite specific
    'innovate',
    'users',
    'topics',
    'projects',
    'events',
    'activity',
    'challenges',
    'ignite',
    'voting',
    'timeslot',
    'webcast',
    'ignite_resources',
    'badges',
    'awards',
    'blogs',
    'search',
)

# Tells the extract script what files to look for L10n in and what function
# handles the extraction. The Tower library expects this.
DOMAIN_METHODS = {
    'messages': [
        ('apps/**.py',
            'tower.management.commands.extract.extract_tower_python'),
        ('**/templates/**.html',
            'tower.management.commands.extract.extract_tower_template'),
    ],

    ## Use this if you have localizable HTML files:
    #'lhtml': [
    #    ('**/templates/**.lhtml',
    #        'tower.management.commands.extract.extract_tower_template'),
    #],

    ## Use this if you have localizable JS files:
    #'javascript': [
        # Make sure that this won't pull in strings from external libraries you
        # may use.
    #    ('media/js/**.js', 'javascript'),
    #],
}

# Path to Java. Used for compress_assets.
JAVA_BIN = '/usr/bin/java'

## Auth
PWD_ALGORITHM = 'bcrypt'
HMAC_KEYS = {
    #'2011-01-01': 'cheesecake',
}

## Tests
TEST_RUNNER = 'test_utils.runner.RadicalTestSuiteRunner'

## Celery
CELERY_RESULT_BACKEND = 'amqp'
CELERY_IGNORE_RESULT = True

MAX_FILEPATH_LENGTH = 250

# a list of passwords that meet policy requirements, but are considered
# too common and therefore easily guessed.
PASSWORD_BLACKLIST = (
    'trustno1',
    'access14',
    'rush2112',
    'p@$$w0rd',
    'abcd1234',
    'qwerty123',
)

AUTH_PROFILE_MODULE = 'users.Profile'

# Email goes to the console by default.  s/console/smtp/ for regular delivery
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_BACKEND = 'django_mailer.smtp_queue.EmailBackend'
DEFAULT_FROM_EMAIL = 'Innovate Mozilla <innovate@mozilla.org>'
SERVER_EMAIL = 'Innovate Mozilla <innovate@mozilla.org>'

AUTHENTICATION_BACKENDS = (
    'django_browserid.auth.BrowserIDBackend',
    'django.contrib.auth.backends.ModelBackend',
    'challenges.auth.SubmissionBackend'
)

BROWSERID_VERIFICATION_URL = 'https://browserid.org/verify'
BROWSERID_CREATE_USER = True
BROWSERID_DISABLE_CERT_CHECK = True
LOGIN_REDIRECT_URL = '/'
LOGIN_REDIRECT_URL_FAILURE = '/'

PUSH_DEFAULT_HUB = 'http://superfeedr.com/hubbub'
PUSH_DEFAULT_HUB_USERNAME = ''
PUSH_DEFAULT_HUB_PASSWORD = ''
PUSH_CREDENTIALS = 'projects.utils.push_hub_credentials'

SOUTH_TESTS_MIGRATE = False

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

# Don't cache count queries at all, because there's no way to invalidate them
CACHE_COUNT_TIMEOUT = None

GRAVATAR_URL = 'https://secure.gravatar.com/avatar/'

SITE_FEED_URLS = {
    'splash': 'https://blog.mozillaignite.org/feed/',
}

JUDGES_PER_SUBMISSION = 2

# Switch for the development phase
DEVELOPMENT_PHASE = False


# TimeSlot Booking
# Time to expire the booking if not confirmed
BOOKING_EXPIRATION = 5 * 60   # 5 minutes
# Determines if the user throttling will be enabled
BOOKING_THROTTLING = False
# Email preferences
BOOKING_SEND_EMAILS = True

# Paginator
PAGINATOR_SIZE = 25

MIDDLEWARE_URL_EXCEPTIONS = [
    '/__debug__/',
    '/admin/',
    MEDIA_URL,
    ]

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': 'http://127.0.0.1:9200/',
        'INDEX_NAME': 'haystack',
        'TIMEOUT': 60 * 5,
    },
}

# High number since we don't want pagination
HAYSTACK_SEARCH_RESULTS_PER_PAGE = 6
HAYSTACK_DEFAULT_OPERATOR = 'AND'

SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True

ANON_ALWAYS = True

