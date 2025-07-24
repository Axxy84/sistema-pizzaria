"""
Configurações para testes - desabilita debug toolbar
"""
from DjangoProject.settings import *

# Remover debug_toolbar dos apps instalados para testes
INSTALLED_APPS = [app for app in INSTALLED_APPS if app != 'debug_toolbar']

# Remover middleware do debug_toolbar
MIDDLEWARE = [m for m in MIDDLEWARE if 'debug_toolbar' not in m]

# Usar banco de testes do Supabase
# Os testes devem usar um banco separado no Supabase
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': os.getenv('DATABASE_HOST', 'aws-0-sa-east-1.pooler.supabase.com'),
        'NAME': 'test_' + os.getenv('DATABASE_NAME', 'postgres'),
        'USER': os.getenv('DATABASE_USER', 'postgres.aewcurtmikqelqykpqoa'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD', 'sua_senha_aqui'),
        'PORT': os.getenv('DATABASE_PORT', '5432'),
        'OPTIONS': {
            'sslmode': 'require',
        },
        'TEST': {
            'NAME': 'test_pizzaria_db',
        }
    }
}