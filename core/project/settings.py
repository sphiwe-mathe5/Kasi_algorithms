import os
from pathlib import Path
from decouple import config, Csv
from google.oauth2 import service_account

BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_DIR = Path(__file__).resolve().parent

SECRET_KEY = config('SECRET_KEY')
DEBUG = False
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='.vercel.app,127.0.0.1,.com').split(',')
ADMIN_PATH = config('ADMIN_PATH')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'whitenoise.runserver_nostatic',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_otp',
    'django_otp.plugins.otp_totp',
    'core',
    'submit',
    'emails',
    'crispy_forms',
    'axes',
    #'crispy_bootstrap4',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django_otp.middleware.OTPMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'axes.middleware.AxesMiddleware',
]

ROOT_URLCONF = 'core.project.urls'


#WSGI_APPLICATION = 'core.project.wsgi.application'
ASGI_APPLICATION = 'core.project.asgi.application'


CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    },
}

CRISPY_TEMPLATE_PACK = 'bootstrap4'  # or 'bootstrap3' depending on your Bootstrap version


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]






DATABASES = {
    'default': {
        'ENGINE': config('DATABASE_ENGINE'),
        'NAME': config('DATABASE_NAME'),
        'USER': config('DATABASE_USER'),
        'PASSWORD': config('DATABASE_PASSWORD'),
        'HOST': config('DATABASE_HOST'),
        'PORT': config('DATABASE_PORT'),
    }
}

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

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Johannesburg'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

AUTHENTICATION_BACKENDS = [
    'axes.backends.AxesStandaloneBackend',
    'django.contrib.auth.backends.ModelBackend',
]

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, "project/static")]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"




DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
GS_PROJECT_ID = config('GS_PROJECT_ID')
GS_BUCKET_NAME = config('GS_BUCKET_NAME')
MEDIA_ROOT = "media/"
UPLOAD_ROOT = 'media/uploads'
MEDIA_URL = config('MEDIA_URL')

GS_CREDENTIALS = service_account.Credentials.from_service_account_info({
    "type": config("GOOGLE_CLOUD_TYPE", default="service_account"),
    "project_id": config("GOOGLE_CLOUD_PROJECT_ID"),
    "private_key_id": config("GOOGLE_CLOUD_PRIVATE_KEY_ID"),
    "private_key": config("GOOGLE_CLOUD_PRIVATE_KEY").replace("\\n", "\n"),
    "client_email": config("GOOGLE_CLOUD_CLIENT_EMAIL"),
    "client_id": config("GOOGLE_CLOUD_CLIENT_ID"),
    "auth_uri": config("GOOGLE_CLOUD_AUTH_URI", default="https://accounts.google.com/o/oauth2/auth"),
    "token_uri": config("GOOGLE_CLOUD_TOKEN_URI", default="https://oauth2.googleapis.com/token"),
    "auth_provider_x509_cert_url": config("GOOGLE_CLOUD_AUTH_PROVIDER_X509_CERT_URL", default="https://www.googleapis.com/oauth2/v1/certs"),
    "client_x509_cert_url": config("GOOGLE_CLOUD_CLIENT_X509_CERT_URL"),
    "universe_domain": config("GOOGLE_CLOUD_UNIVERSE_DOMAIN", default="googleapis.com")
})


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


EMAIL_BACKEND = config('EMAIL_BACKEND')
EMAIL_PORT = config('EMAIL_PORT')
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = config('ADMIN_EMAIL')
EMAIL_USE_SSL = config('EMAIL_USE_SSL')
ADMIN_EMAIL = config('ADMIN_EMAIL')


SILENCED_SYSTEM_CHECKS = config('SILENCED_SYSTEM_CHECKS', cast=Csv())

AXES_FAILURE_LIMIT = config('AXES_FAILURE_LIMIT', cast=int)

AXES_COOLOFF_TIME = 1

AXES_ONLY_ADMIN_SITE = config('AXES_ONLY_ADMIN_SITE', cast=bool)

AXES_LOCKOUT_TEMPLATE = config('AXES_LOCKOUT_TEMPLATE')

AXES_LOCKOUT_URL = config('AXES_LOCKOUT_URL')
AXES_USERNAME_FORM_FIELD = config('AXES_USERNAME_FORM_FIELD')

AXES_RESET_ON_SUCCESS = config('AXES_RESET_ON_SUCCESS', cast=bool)

AXES_NEVER_LOCKOUT_WHITELIST = config('AXES_NEVER_LOCKOUT_WHITELIST',
                                      cast=bool)
AXES_IP_WHITELIST = config('AXES_IP_WHITELIST', cast=Csv())

AXES_ENABLE_ACCESS_FAILURE_LOG = config('AXES_ENABLE_ACCESS_FAILURE_LOG',
                                        cast=bool)

AXES_RESET_ON_SUCCESS = config('AXES_RESET_ON_SUCCESS', cast=bool)

AXES_LOCKOUT_PARAMETERS = config('AXES_LOCKOUT_PARAMETERS', cast=Csv())


LOGIN_REDIRECT_URL = 'index'
LOGIN_URL = 'login'