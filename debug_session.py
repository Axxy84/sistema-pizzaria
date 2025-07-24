#!/usr/bin/env python
"""
Debug de sessão Django + Supabase
"""

import os
import django
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoProject.settings')
django.setup()

from django.test import Client
from apps.authentication.backends import SupabaseBackend

def debug_session():
    print("=== DEBUG DE SESSÃO E LOGIN ===\n")
    
    # 1. Criar cliente de teste
    client = Client()
    
    # 2. Fazer login via POST
    print("1. Tentando login via POST:")
    response = client.post('/auth/login/', {
        'email': 'admin@pizzaria.com',
        'password': 'admin8477thygas'
    }, follow=False)  # Não seguir redirecionamentos
    
    print(f"   - Status: {response.status_code}")
    print(f"   - Location: {response.get('Location', 'Nenhum redirecionamento')}")
    
    # Verificar cookies
    print("\n2. Cookies definidos:")
    for cookie_name, cookie in client.cookies.items():
        print(f"   - {cookie_name}: {cookie.value[:20]}...")
    
    # 3. Verificar sessão após login
    print("\n3. Fazendo GET na home após login:")
    response = client.get('/')
    
    print(f"   - User: {response.wsgi_request.user}")
    print(f"   - Autenticado: {response.wsgi_request.user.is_authenticated}")
    
    # 4. Verificar sessão diretamente
    print("\n4. Dados da sessão:")
    from django.contrib.sessions.models import Session
    from django.utils import timezone
    
    sessions = Session.objects.filter(expire_date__gt=timezone.now())
    print(f"   - Sessões ativas: {sessions.count()}")
    
    for session in sessions[:3]:  # Mostrar até 3 sessões
        data = session.get_decoded()
        print(f"   - Session {session.session_key[:10]}...")
        print(f"     _auth_user_id: {data.get('_auth_user_id')}")
        print(f"     _auth_user_backend: {data.get('_auth_user_backend')}")
    
    # 5. Testar backend diretamente
    print("\n5. Testando backend Supabase diretamente:")
    backend = SupabaseBackend()
    from django.test import RequestFactory
    request = RequestFactory().post('/auth/login/')
    
    user = backend.authenticate(request, username='admin@pizzaria.com', password='admin8477thygas')
    if user:
        print(f"   ✓ Backend retornou usuário: {user}")
        print(f"   - Username: {user.username}")
        print(f"   - Email: {user.email}")
        print(f"   - ID: {user.id}")
        print(f"   - Ativo: {user.is_active}")
    else:
        print("   ✗ Backend retornou None")
    
    # 6. Verificar configurações
    print("\n6. Configurações Django:")
    from django.conf import settings
    print(f"   - MIDDLEWARE com SessionMiddleware: {'django.contrib.sessions.middleware.SessionMiddleware' in settings.MIDDLEWARE}")
    print(f"   - MIDDLEWARE com AuthenticationMiddleware: {'django.contrib.auth.middleware.AuthenticationMiddleware' in settings.MIDDLEWARE}")
    print(f"   - INSTALLED_APPS com sessions: {'django.contrib.sessions' in settings.INSTALLED_APPS}")
    print(f"   - INSTALLED_APPS com auth: {'django.contrib.auth' in settings.INSTALLED_APPS}")

if __name__ == '__main__':
    debug_session()