"""
Configurações para testes - desabilita debug toolbar
"""
from DjangoProject.settings import *

# Remover debug_toolbar dos apps instalados para testes
INSTALLED_APPS = [app for app in INSTALLED_APPS if app != 'debug_toolbar']

# Remover middleware do debug_toolbar
MIDDLEWARE = [m for m in MIDDLEWARE if 'debug_toolbar' not in m]

# Usar banco de memória para testes
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}