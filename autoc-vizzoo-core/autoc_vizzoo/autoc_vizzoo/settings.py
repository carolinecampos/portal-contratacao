"""
Django settings for autoc_vizzoo project.

Generated by 'django-admin startproject' using Django 1.11.16.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '=kw5@$2sr2qkn7xu23ag2e_qxrevq^s4=hv70123)1klcu!22e'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [os.environ['ALLOWED_HOSTS']]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'contratacao',
    'rest_framework',
    'rest_framework_swagger',
    'corsheaders',
    'drf_yasg',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.common.BrokenLinkEmailsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

CORS_ORIGIN_ALLOW_ALL = True

ROOT_URLCONF = 'autoc_vizzoo.urls'

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

WSGI_APPLICATION = 'autoc_vizzoo.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.oracle',
        'NAME': os.environ['HOST_NAME'],
        'USER':  os.environ['HOST_USER'],
        'PASSWORD': os.environ['HOST_PASSWORD']
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

SWAGGER_SETTINGS = {
    'DOC_EXPANSION': 'none',
    'DEEP_LINKING': True
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [],
    'DEFAULT_AUTHENTICATION_CLASSES': []
}

#dados de acesso aos serviços do vizzzo
VIZZO_URL = os.environ['VIZZO_URL']
VIZZOO_URL_GET_TOKEN = os.environ['VIZZOO_URL_GET_TOKEN']
VIZZOO_MANAGER_URL = os.environ['VIZZOO_MANAGER_URL']
VIZZOO_SSO_CLIENT_SECRET = os.environ['VIZZOO_SSO_CLIENT_SECRET']

#serviços do commander
COMMANDER_URL = os.environ['COMMANDER_URL']
COMMANDER_USER = os.environ['COMMANDER_USER']
COMMANDER_PASS = os.environ['COMMANDER_PASS']

#serviços do gensky
GENSKY_URL = os.environ['GENSKY_URL']
GENSKY_USER = os.environ['GENSKY_USER']
GENSKY_PASS = os.environ['GENSKY_PASS']

#serviço de envio de email
NOTIFIER_SENDER = os.environ['NOTIFIER_SENDER']

#link autoimplantacao
CONFIRMAR_DADOS_USUARIO = os.environ['CONFIRMAR_DADOS_USUARIO']

#gateway
GATEWAY_URL = os.environ['GATEWAY_URL']
GATEWAY_SECRET = os.environ['GATEWAY_SECRET']
GATEWAY_REQUEST_ID = os.environ['GATEWAY_REQUEST_ID']

#auto_contratacao
AUTOCONTRATACAO_URL = os.environ['AUTOCONTRATACAO_URL']
