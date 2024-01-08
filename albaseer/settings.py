import environ
import os
from pathlib import Path
from django.conf.locale.en import formats as en_formats
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from datetime import timedelta

env = environ.Env()
env.read_env()
DEBUG = env('DEBUG',cast=bool)
# print(DEBUG)
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
BASE_URL = "https://stage-api-al-baseer.alnafi.com/"


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-1i*4dn)-_9)gf84&yqq1jytyu$6ob98k0u!$+bha%8wv!i#v6w'

# SECURITY WARNING: don't run with debug turned on in production!cl
# DEBUG = env("DEBUG")

if not DEBUG:
    REST_FRAMEWORK = {
        'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
        'PAGE_SIZE': 10,
        'DEFAULT_LINKS_TEMPLATE': 'rest_framework/pagination/links.html',
        'BASE_URL': 'https://stage-api-al-baseer.alnafi.com/'
    }


# Change date format (AM PM to hours time format)
en_formats.DATE_FORMAT = 'Y-m-d'
en_formats.TIME_FORMAT = 'H:i:s'
en_formats.DATETIME_FORMAT = 'Y-m-d H:i:s'


ALLOWED_HOSTS = ["*"]
CORS_ALLOW_ALL_ORIGINS: bool

CORS_ALLOWED_ORIGINS = [
    "https://example.com",
    "https://sub.example.com",
    "http://localhost:3000",
    "http://127.0.0.1:9000",
    "http://127.0.0.1:8000",
    'https://stage-api-al-baseer.alnafi.com',
    'http://stage-api-al-baseer.alnafi.com',
    'http://ec2-34-194-10-51.compute-1.amazonaws.com',
    'https://ec2-34-194-10-51.compute-1.amazonaws.com',
    'http://stage-al-baseer.alnafi.com',
    'https://stage-al-baseer.alnafi.com',
    'http://ec2-3-233-91-36.compute-1.amazonaws.com',
    'https://al-baseer.alnafi.com',
    'https://api-al-baseer.alnafi.com',
    'http://ec2-52-6-12-123.compute-1.amazonaws.com',
    'https://e6ea-124-29-228-160.ngrok-free.app',
    'https://ec2-18-217-108-10.us-east-2.compute.amazonaws.com',
    'http://ec2-18-217-108-10.us-east-2.compute.amazonaws.com',
    'http://18.217.108.10'
]

CSRF_TRUSTED_ORIGINS = ['https://stage-api-al-baseer.alnafi.com',
                        'https://7943-2407-aa80-14-8f15-3ec1-e258-e992-b24a.ngrok.io',
                        'http://ec2-3-233-91-36.compute-1.amazonaws.com',
                        'https://al-baseer.alnafi.com',
                        'https://api-al-baseer.alnafi.com',
                        'http://ec2-52-6-12-123.compute-1.amazonaws.com',
                        'https://ec2-18-217-108-10.us-east-2.compute.amazonaws.com',
                        'http://ec2-18-217-108-10.us-east-2.compute.amazonaws.com',
                        'http://18.217.108.10',
                        'https://e6ea-124-29-228-160.ngrok-free.app']


REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '1/minute',
    }
}


CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]
CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'rest_framework_swagger',
    'import_export',
    'rangefilter',
    'django_crontab',



    'accounts.apps.AccountsConfig',
    'payment.apps.PaymentConfig',
    'feedback.apps.FeedbackConfig',
    'security.apps.SecurityConfig',
    'chatwoot.apps.ChatwootConfig',
    'user.apps.UserConfig',
    'thinkific.apps.ThinkificConfig',
    'products.apps.ProductsConfig',
    'trainers.apps.TrainersConfig',
    'newsletter.apps.NewsletterConfig',
    'stream.apps.StreamConfig',
    'affiliate.apps.AffiliateConfig',
    "corsheaders",
    "secrets_api",
]

CRONJOBS = [
    ('0 0 * * *', 'payment.academy_leads.handle'), #24 ghaty ma chaly gi
    ('0 0 * * *', 'payment.renewal_leads.handle'),

]

# '0 0 * * *',
# '* * * * *', 



if DEBUG:
    INSTALLED_APPS += ['debug_toolbar']

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
]

if DEBUG:
    MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware", ]
    INTERNAL_IPS = [
        "127.0.0.1",
    ]


ROOT_URLCONF = 'albaseer.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'albaseer.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases
if DEBUG:
    print("SQL Lite CONNECTED")
    DATABASES = {
        'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    print("RDS CONNECTED")
    # env("DATABASE_ENGINE")c
    DATABASES = {
        'default': {
            'ENGINE': env('DATABASE_ENGINE'),
            'NAME': env("DATABASE_NAME"),
            'USER': env("DATABASE_USER"),
            'PASSWORD': env("DATABASE_PASSWORD").strip(),
            'HOST': env("DATABASE_HOST"),
            'PORT': env('DATABASE_PORT'),
            # 'OPTIONS': {
            #     'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
            # }
        }
    }


# if DEBUG:
#     # CACHES = {
#     #     'default': {
#     #         'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
#     #         'TIMEOUT':1800,
#     #     },
#     # }
#     CACHES = {
#         'default': {
#             'BACKEND': 'django_redis.cache.RedisCache',
#             'LOCATION': 'redis://127.0.0.1:'+str(env("REDIS_PORT", default=6379)), # Change IP and port if needed
#             'TIMEOUT':1,
#             'OPTIONS': {
#                 'CLIENT_CLASS': 'django_redis.client.DefaultClient',
#             }
#         }
#     }
# else:
#     CACHES = {
#         'default': {
#             'BACKEND': 'django_redis.cache.RedisCache',
#             'LOCATION': 'redis://127.0.0.1:'+str(env("REDIS_PORT", default=6379)), # Change IP and port if needed
#             'TIMEOUT':1800,
#             'OPTIONS': {
#                 'CLIENT_CLASS': 'django_redis.client.DefaultClient',
#             }
#         }
#     }
# print(DATABASES)

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

TIME_INPUT_FORMAT = ['%H:%M:%S']



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/


# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny'
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}

REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = [
        'rest_framework.renderers.JSONRenderer',
        # 'rest_framework.renderers.BrowsableAPIRenderer',
]
if DEBUG:
    REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'].append(
        'rest_framework.renderers.BrowsableAPIRenderer',
    )


CSRF_COOKIE_NAME="csrftoken"
CSRF_HEADER_NAME="csrftoken"
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True



MEDIA_URL = '/media/'
STATIC_ROOT = os.path.join(BASE_DIR, "static/")

if DEBUG:
    STATIC_URL = '/static/'
    MEDIA_ROOT = os.path.join(BASE_DIR, "media")
else:
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3StaticStorage'
    AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY")
    AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID")
    AWS_STORAGE_BUCKET_NAME = env("AWS_STORAGE_BUCKET_NAME")
    AWS_QUERYSTRING_AUTH = False
    STATIC_URL = env("S3_STATIC_URL")
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    MEDIA_ROOT = env("S3_MEDIA")


if not DEBUG:
    pass
    sentry_sdk.init(
    dsn="https://e09dae87954440acb4e0c0683b86a2c1@o1153820.ingest.sentry.io/4504926428528640",
    integrations=[
        DjangoIntegration(),
    ],

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)

PASSWORD_RESET_TIMEOUT=900

AUTH_USER_MODEL = 'user.User'

# Email Configuration
EMAIL_BACKEND="django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'faizanahmed14877@gmail.com'
EMAIL_HOST_PASSWORD = 'rrogkbngirfjchbq'
EMAIL_USE_TLS = True

#JWT Settings
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=365),

    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",

    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",

    "JTI_CLAIM": "jti",
    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(days=1),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=365),
    'AUTH_COOKIE': 'access_token',
    'REFRESH_COOKIE': 'refresh_token',
    'AUTH_COOKIE_DOMAIN': None,
    'AUTH_COOKIE_SECURE': False,
    'AUTH_COOKIE_HTTP_ONLY': True,
    'AUTH_COOKIE_PATH': '/',        # The path of the auth cookie.
    # The SameSite attribute of the auth cookie.
    'AUTH_COOKIE_SAMESITE': "Lax",


    "TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainPairSerializer",
    "TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSerializer",
    "TOKEN_VERIFY_SERIALIZER": "rest_framework_simplejwt.serializers.TokenVerifySerializer",
    "TOKEN_BLACKLIST_SERIALIZER": "rest_framework_simplejwt.serializers.TokenBlacklistSerializer",
    "SLIDING_TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainSlidingSerializer",
    "SLIDING_TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSlidingSerializer",
}


FILE_UPLOAD_MAX_MEMORY_SIZE = 15875938475934
DATA_UPLOAD_MAX_NUMBER_FIELDS = 1583795834

EXCHANGE_RATE_API_KEY = '6b253c10180740ec36a3b5c8'
CRM_COUNTRY_TAX_API= env('CRM_COUNTRY_TAX_API',default="")



# if DEBUG:
#     EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
#     EMAIL_HOST = 'smtp.mailtrap.io'
#     EMAIL_HOST_USER = 'b688d22fbcecbf'
#     EMAIL_HOST_PASSWORD = '8992648cb5dd18'
#     EMAIL_PORT = '2525'
#     EMAIL_USE_TLS = True
#     EMAIL_USE_SSL = False

# else:
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_BACKEND = 'django_ses.SESBackend'
# MAIL_MAILER=env("MAIL_MAILER")
MAIL_HOST=env("MAIL_HOST")
AWS_SECRET_ACCESS_KEY = env("EMAIL_AWS_SECRET_ACCESS_KEY")
AWS_ACCESS_KEY_ID = env("EMAIL_AWS_ACCESS_KEY_ID")
# MAIL_PORT=env("MAIL_PORT")
# MAIL_USERNAME=env("MAIL_USERNAME")
# MAIL_PASSWORD=env("MAIL_PASSWORD")
# MAIL_ENCRYPTION=env("MAIL_ENCRYPTION")
# MAIL_FROM_ADDRESS=env("MAIL_FROM_ADDRESS")
