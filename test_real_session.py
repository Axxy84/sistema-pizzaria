#!/usr/bin/env python
"""
Teste real da sessão com usuário válido
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoProject.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User

def test_real_login():
    """Testa login real com usuário com senha"""
    print("=== TESTE REAL DE LOGIN ===")
    
    # Usuário de teste
    username = 'test@test.com'
    password = 'test123'
    
    user = User.objects.get(username=username)
    print(f"Testando com: {user.username}")
    
    # Client de teste
    client = Client()
    
    # 1. Homepage sem login
    print("\n1. Homepage sem login:")
    response = client.get('/')
    print(f"   Usuário: {response.wsgi_request.user}")
    print(f"   Autenticado: {response.wsgi_request.user.is_authenticated}")
    
    # 2. Login usando ModelBackend direto
    print("\n2. Login usando authenticate/login direto:")
    from django.contrib.auth import authenticate, login
    from django.test import RequestFactory
    from django.contrib.sessions.middleware import SessionMiddleware
    from django.contrib.auth.middleware import AuthenticationMiddleware
    
    # Criar request
    factory = RequestFactory()
    request = factory.post('/test/')
    
    # Aplicar middlewares
    session_middleware = SessionMiddleware(lambda r: None)
    session_middleware.process_request(request)
    request.session.save()
    
    auth_middleware = AuthenticationMiddleware(lambda r: None)
    auth_middleware.process_request(request)
    
    # Autenticar
    auth_user = authenticate(request, username=username, password=password)
    print(f"   Authenticate result: {auth_user}")
    
    if auth_user:
        login(request, auth_user)
        print(f"   Após login: {request.user}")
        print(f"   Autenticado: {request.user.is_authenticated}")
        print(f"   Session ID: {request.session.session_key}")
        print(f"   User ID na sessão: {request.session.get('_auth_user_id')}")
    
    # 3. Tentar login via formulário web
    print("\n3. Login via formulário (vai usar Supabase - deve falhar):")
    response = client.post('/auth/login/', {
        'email': username,
        'password': password
    })
    print(f"   Status: {response.status_code}")
    
    # 4. Tentar force login
    print("\n4. Force login:")
    # Atualizar force login para usar nosso usuário de teste
    response = client.get('/force-login/', follow=True)
    print(f"   Status: {response.status_code}")
    
    # Verificar se funcionou
    response = client.get('/')
    print(f"   Após force login - Usuário: {response.wsgi_request.user}")
    print(f"   Autenticado: {response.wsgi_request.user.is_authenticated}")

if __name__ == "__main__":
    test_real_login()