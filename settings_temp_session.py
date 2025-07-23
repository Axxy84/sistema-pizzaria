"""
Configuração temporária para usar sessões em cookies
enquanto a senha do PostgreSQL não é corrigida
"""

# Importar todas as configurações do settings.py
from DjangoProject.settings import *

# Sobrescrever a configuração de sessão para usar cookies
# Isso evita a necessidade de acessar o banco de dados
SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'

# Configurações adicionais de segurança para cookies
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = False  # True em produção com HTTPS
SESSION_COOKIE_SAMESITE = 'Lax'

print("🍪 USANDO SESSÕES EM COOKIES (TEMPORÁRIO)")
print("⚠️  IMPORTANTE: Corrija a senha do PostgreSQL no .env")
print("⚠️  DATABASE_PASSWORD deve ser a senha correta do Supabase")