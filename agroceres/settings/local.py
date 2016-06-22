from .base import *


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': ‘usuario’,
        'USER': ‘usuario’,
        'PASSWORD’:’123’,
        'HOST':'localhost',
        'PORT’:’4234’,
    }
}

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    BASE_DIR.child('static'),
)

#from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP
#TEMPLATE_CONTEXT_PROCESSORS=TCP+(
 #       'apps.ceres.processors.globalVars',
   #     'django.contrib.messages.context_processors.messages',
  #      'django.core.context_processors.request',
   # )

AUTHENTICATION_BACKENDS=(
    'social.backends.facebook.FacebookAppOAuth2',
    'social.backends.facebook.FacebookOAuth2',
    'social.backends.twitter.TwitterOAuth',
    'social.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_LOGIN_REDIRECT_URL='home'
SOCIAL_AUTH_USER_MODEL='account.User'

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY='8account.google’
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET=‘sadsdasdasd-‘

SOCIAL_AUTH_TWITTER_KEY=‘asdasdas’
SOCIAL_AUTH_TWITTER_SECRET=‘asdasdas’

SOCIAL_AUTH_FACEBOOK_KEY=‘32434’
SOCIAL_AUTH_FACEBOOK_SECRET=‘dasdasd’

SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = ['email']
SOCIAL_AUTH_PIPELINE=(
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    'social.pipeline.user.get_username',
    'social.pipeline.social_auth.associate_by_email',  # <--- enable this one
    'social.pipeline.user.create_user',
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.social_auth.load_extra_data',
    'apps.account.pipeline.user_details',
)

MEDIA_URL='/media/'
MEDIA_ROOT=BASE_DIR.child('media')
