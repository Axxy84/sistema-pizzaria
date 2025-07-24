"""
Script para corrigir o erro de middleware
Remove referências ao middleware_temp que não existe mais
"""
import os
import sys

# Adiciona o projeto ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Define as configurações do Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoProject.settings')

# Importa Django
import django
django.setup()

from django.conf import settings

print("=== CORRIGINDO MIDDLEWARE ===")
print("\nMiddleware atual:")
for m in settings.MIDDLEWARE:
    print(f"  - {m}")

# Remove middleware problemático
middleware_to_remove = [
    'apps.authentication.middleware_temp',
    'apps.authentication.middleware.NoAuthMiddleware',  # Versão antiga
]

# Lista correta de middleware
correct_middleware = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'apps.core.middleware.NoAuthMiddleware',  # Middleware correto
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

print("\n=== MIDDLEWARE CORRIGIDO ===")
print("\nAdicione isso ao seu settings.py:")
print("\nMIDDLEWARE = [")
for m in correct_middleware:
    print(f"    '{m}',")
print("]")

print("\n=== VERIFICANDO ARQUIVOS ===")

# Verifica se o middleware correto existe
if os.path.exists('apps/core/middleware.py'):
    print("✅ apps/core/middleware.py existe")
else:
    print("❌ apps/core/middleware.py NÃO existe")

if os.path.exists('apps/authentication/middleware_temp.py'):
    print("❌ apps/authentication/middleware_temp.py existe (deve ser removido)")
else:
    print("✅ apps/authentication/middleware_temp.py não existe (correto)")

print("\n=== INSTRUÇÕES ===")
print("1. Abra DjangoProject/settings.py")
print("2. Encontre a seção MIDDLEWARE")
print("3. Substitua toda a lista MIDDLEWARE pela lista acima")
print("4. Salve o arquivo")
print("5. Execute o servidor novamente")