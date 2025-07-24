"""
Django settings otimizado para máxima performance
Sem autenticação, focado em velocidade
"""

from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-fast-performance-key'

DEBUG = True

ALLOWED_HOSTS = ['*']

# Apps mínimos necessários
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',  # Necessário para o Django funcionar
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'django_filters',
    'apps.produtos',
    'apps.pedidos', 
    'apps.clientes',
    'apps.estoque',
    'apps.financeiro',
    'apps.dashboard',
    'settings',
]

# Middleware mínimo
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.gzip.GZipMiddleware',
]

ROOT_URLCONF = 'DjangoProject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
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

WSGI_APPLICATION = 'DjangoProject.wsgi.application'

# Database - APENAS SUPABASE
import dj_database_url

DATABASE_URL = os.getenv('DATABASE_URL', 
    f"postgresql://{os.getenv('DATABASE_USER', 'postgres.aewcurtmikqelqykpqoa')}:"
    f"{os.getenv('DATABASE_PASSWORD', 'sua_senha_aqui')}@"
    f"{os.getenv('DATABASE_HOST', 'aws-0-sa-east-1.pooler.supabase.com')}:"
    f"{os.getenv('DATABASE_PORT', '5432')}/"
    f"{os.getenv('DATABASE_NAME', 'postgres')}?sslmode=require"
)

DATABASES = {
    'default': dj_database_url.parse(DATABASE_URL, conn_max_age=600)
}

# Cache em memória - mais rápido
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
        'TIMEOUT': 300,
        'OPTIONS': {
            'MAX_ENTRIES': 1000,
        }
    }
}

# Sessões em cache
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'

# Internacionalização
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = False  # Desabilitado para performance
USE_TZ = True

# Static files
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Whitenoise para servir estáticos
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# REST Framework simplificado
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ],
    'DEFAULT_PAGINATION_CLASS': None,
}

# CORS
CORS_ALLOW_ALL_ORIGINS = True

# Performance
DATA_UPLOAD_MAX_NUMBER_FIELDS = 1000
CONN_MAX_AGE = 600

# Desabilitar recursos desnecessários
USE_L10N = False
USE_THOUSAND_SEPARATOR = False

# Senha para cancelamento
ADMIN_CANCEL_PASSWORD = '2024pizza'