"""
Configurações temporárias SEM AUTENTICAÇÃO
ATENÇÃO: APENAS PARA DESENVOLVIMENTO LOCAL!
"""

# Importar todas as configurações padrão
from DjangoProject.settings import *

print("\n" + "="*60)
print("⚠️  ATENÇÃO: SISTEMA RODANDO SEM AUTENTICAÇÃO!")
print("⚠️  ISSO É APENAS PARA DESENVOLVIMENTO LOCAL!")
print("⚠️  NUNCA USE EM PRODUÇÃO!")
print("="*60 + "\n")

# Adicionar o middleware de bypass ANTES do AuthenticationMiddleware
MIDDLEWARE_POSITION = MIDDLEWARE.index('django.contrib.auth.middleware.AuthenticationMiddleware')
MIDDLEWARE.insert(MIDDLEWARE_POSITION + 1, 'apps.authentication.middleware_temp.BypassAuthMiddleware')

# Usar sessões em cookies para evitar o banco de dados
SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'

# Desabilitar a verificação de CSRF temporariamente
MIDDLEWARE = [m for m in MIDDLEWARE if m != 'django.middleware.csrf.CsrfViewMiddleware']

# Configurações para facilitar o desenvolvimento
DEBUG = True
ALLOWED_HOSTS = ['*']

# Desabilitar login_required em todas as views
LOGIN_URL = '/'
LOGIN_REDIRECT_URL = '/'

print("Configurações aplicadas:")
print("✅ Middleware de bypass de autenticação ativo")
print("✅ Sessões em cookies (sem banco de dados)")
print("✅ CSRF desabilitado temporariamente")
print("✅ Todas as páginas acessíveis sem login")
print("\nUsuário temporário criado:")
print("- Username: temp_user")
print("- Email: temp@pizzaria.com")
print("- Permissões: Superusuário (acesso total)")
print("\n" + "="*60 + "\n")