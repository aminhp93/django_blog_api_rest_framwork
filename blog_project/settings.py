"""
Django settings for blog_project project.

Generated by 'django-admin startproject' using Django 1.10.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '08dk$0t0=wd5^b#5+v1wyp3u!r#y%80pq*mhk%08ok!!r3#s61'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',
    'comments',
    'crispy_forms',
    'markdown_deux',
    'pagedown',
    'posts',
    'rest_framework',
]

CRISPY_TEMPLATE_PACK = 'bootstrap3'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'blog_project.urls'

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

WSGI_APPLICATION = 'blog_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


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


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/
LOGIN_URL = '/login/'

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

STATIC_ROOT = os.path.join(BASE_DIR, "static_cdn")

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media_cdn")
# MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), "media_cdn")

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    # 'DEFAULT_PARSER_CLASSES': (
    #     'rest_framework.parsers.JSONParser',
    # ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    )
}

"""

curl -X POST -d "username=amin&password=Miamikki521" http://localhost:8000/api/auth/token/

eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE0ODQ1MDIxNDEsInVzZXJuYW1lIjoiYW1pbiIsInVzZXJfaWQiOjEsImVtYWlsIjoibWluaEBnbWFpbC5jb20ifQ.K5MPldXt-fpjgezZYeXxkQS-1cQ_oJnD8RZ5_dW3BZ4

curl -H "Authorization: JWT eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE0ODQ1MDIxNDEsInVzZXJuYW1lIjoiYW1pbiIsInVzZXJfaWQiOjEsImVtYWlsIjoibWluaEBnbWFpbC5jb20ifQ.K5MPldXt-fpjgezZYeXxkQS-1cQ_oJnD8RZ5_dW3BZ4" http://localhost:8000/api/comments/

curl -X POST -H "Content-Type: application/json" -d '{"username":"admin","password":"password123"}' http://localhost:8000/api-token-auth/

curl -X POST -H "Authorization: JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6Im1pbmhAZ21haWwuY29tIiwidXNlcm5hbWUiOiJhbWluIiwidXNlcl9pZCI6MSwiZXhwIjoxNDg0NTAyOTA4fQ.wUlbB8XFbZdec55Bt4OD3BYBsY2PQoqo4kySpkcXg3A" -H "Content-Type: application/json" -d '{"content":"this is some content"}' http://localhost:8000/api/comments/create/?slug=test&type=posts

curl http://localhost:8000/api/comments/


"""

