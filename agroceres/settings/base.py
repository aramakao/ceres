from unipath import Path

BASE_DIR = Path(__file__).ancestor(3)
SECRET_KEY = '$key’

DEBUG = True

#TEMPLATE_DEBUG = True
SITE_ID = 1
ALLOWED_HOSTS = ['*']

DJANGO_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.sitemaps',)

LOCAL_APPS = (
    'apps.extras',
    'apps.account',
    'apps.ceres',
    'apps.product',
    'apps.store',
    'apps.api',
    'apps.groups',
    'apps.message',
    'apps.farm',
    'apps.blog',
    'apps.comments',
    'apps.search',
    'apps.reports',
    'apps.meter',
)

THIRD_PARTY_APPS = (
    'unipath',
    'psycopg2',
    'social.apps.django_app.default',
    'rest_framework',
    'rest_framework.authtoken',
    'djoser',
    'django_extensions',
    'notifications',
    'easy_pdf',
    'kombu.transport.django',
)

INSTALLED_APPS = DJANGO_APPS + LOCAL_APPS + THIRD_PARTY_APPS

from django.core.urlresolvers import reverse_lazy
LOGIN_URL = reverse_lazy('account:login')
LOGIN_REDIRECT_URL=reverse_lazy('home')
LOGOUT_URL=reverse_lazy('account:logout')
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'apps.ceres.middleware.SocialAuthExceptionMiddleware',
)

ROOT_URLCONF = 'agroceres.urls'

AUTH_PROFILE_MODULE='apps.users.UserProfile'

WSGI_APPLICATION = 'agroceres.wsgi.application'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS':['templates',],
	'APP_DIRS': False,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
		        'apps.ceres.processors.globalVars',
            ],
            'loaders': [
                ('django.template.loaders.cached.Loader', [
                    'django.template.loaders.filesystem.Loader',
                    'django.template.loaders.app_directories.Loader',
                ]),
            ],
        },
    },
]

#from django.core.mail import EmailMessage
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = False
EMAIL_HOST = ‘mail.com’
EMAIL_PORT = 26
EMAIL_HOST_USER = 'agroceres@mail’
EMAIL_HOST_PASSWORD = ‘asdasdsdasd’
PASSWORD_RESET_TIMEOUT_DAYS=1

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
SERVER_EMAIL = EMAIL_HOST_USER

LANGUAGE_CODE = 'es-co'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
AUTH_USER_MODEL='account.User'

SITE_URL='www.agroceres.org'
SITE_NAME='AgroCeres'
SITE_DOMAIN='www.agroceres.org'

CELERY_ACCEPT_CONTENT = ['pickle','json','msgpack','yaml']
CELERY_TIMEZONE = TIME_ZONE
BROKER_URL = 'django://'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
}

DJOSER = {
    'DOMAIN': 'agroceres.org',
    'SITE_NAME': 'AgroCeres',
    'PASSWORD_RESET_CONFIRM_URL': 'cuenta/recordar/{uid}-{token}/',
    'ACTIVATION_URL': '#/activate/{uid}/{token}',
}
