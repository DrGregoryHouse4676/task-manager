from .base import *


DEBUG = False



RENDER_HOSTNAME = os.getenv('RENDER_EXTERNAL_HOSTNAME')

ALLOWED_HOSTS = [RENDER_HOSTNAME] if RENDER_HOSTNAME else []

CSRF_TRUSTED_ORIGINS = [f"https://{RENDER_HOSTNAME}"] if RENDER_HOSTNAME else []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB'),
        'USER': os.getenv('POSTGRES_USER'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'HOST': os.getenv('POSTGRES_HOST'),
        'PORT': os.getenv('POSTGRES_DB_PORT', 5432),
        'OPTIONS': {'sslmode': 'require'},
    }
}

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True