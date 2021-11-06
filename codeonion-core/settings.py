"""
Django settings for codeonion-core project.

Generated by 'django-admin startproject' using Django 3.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import os
import boto3
import botocore


def get_ssm_key(name):
    ssm = boto3.client('ssm')
    try:
        key = ssm.get_parameter(Name=name, WithDecryption=True)
        return key['Parameter']['Value']
    except botocore.exceptions.ClientError as error:
        return error
    
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# def populate_environ_from_ssm():
#     import os
#     ssm_param_path = os.getenv('AWS_SYSTEMS_MANAGER_PARAM_STORE_PATH')
#     if not ssm_param_path:
#         return
#     import boto3
#     client = boto3.client('ssm')
#     response = client.get_parameters_by_path(Path=ssm_param_path, WithDecryption=True)
#     for param in response['Parameters']:
#         env_name = os.path.basename(param['Name'])
#         os.environ[env_name] = param['Value']


# populate_environ_from_ssm()
# https://github.com/Miserlou/Zappa/issues/1432
# https://engineering.instawork.com/django-settings-in-the-cloud-aa3fc547a2b4

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/


# SECURITY WARNING: don't run with debug turned on in production!

USE_POSTGRES = os.getenv('USE_POSTGRES', False)  # this should be removed later
if os.environ.get('AWS_REGION'): # Check whether AWS_REGION variable exists to see if running in AWS or locally
    LOCAL_TEST = False
    DEBUG = os.environ.get('DJANGO_DEBUG', False)
else:
    LOCAL_TEST = True
    DEBUG = os.getenv('DJANGO_DEBUG', True)
    

#  LOCAL_CONFIG = os.getenv('LOCAL_CONFIG', True)  # this should be removed for pulling info from AWS Parameter Store

# SECURITY WARNING: keep the secret key used in production secret!
if str(LOCAL_TEST) == 'True':
    SECRET_FILE = os.path.join(BASE_DIR, 'secret_key.txt')
    with open(SECRET_FILE) as f:
        SECRET_KEY = f.read().strip()
else:
    SECRET_KEY = get_ssm_key('CODEONION_CORE_TEST_SECRET_KEY')
    # SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')

ALLOWED_HOSTS = ['ntya7jwylf.execute-api.us-east-2.amazonaws.com','127.0.0.1']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',



    # application apps
    'main',
    'scanner',
    'reporter',

    # third party tools
    'rest_framework',

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

ROOT_URLCONF = 'codeonion-core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],  # templates at root level. We may want to place separate templates in each app...,
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


WSGI_APPLICATION = 'codeonion-core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

if str(LOCAL_TEST) == 'True' and str(USE_POSTGRES) != 'True':
    DB_PATH = BASE_DIR
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(DB_PATH, 'db.sqlite3'),
        }
    }
else:
    if str(LOCAL_TEST) == 'True' and str(USE_POSTGRES) == 'True':  # read from local files
        import json
        with open('postgres_env.json') as j_conf:
            db_params = json.load(j_conf)
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql_psycopg2',
                'NAME': db_params["postgres_db"],
                'USER': db_params["postgres_user"],
                'PASSWORD': db_params["postgres_password"],
                'HOST': db_params["postgres_host"],
                'PORT': '5432',
            }
        }
    else:  #read from environment variables
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql_psycopg2',
                'NAME': get_ssm_key('CODEONION_CORE_TEST_POSTGRES_DB'),
                'USER': get_ssm_key('CODEONION_CORE_POSTGRES_USER'),
                'PASSWORD': get_ssm_key('CODEONION_CORE_POSTGRES_PASSWORD'),
                'HOST': get_ssm_key('CODEONION_CORE_POSTGRES_HOST'),
                'PORT': '5432',
            }
        }

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
