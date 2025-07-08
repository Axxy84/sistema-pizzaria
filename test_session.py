#!/usr/bin/env python
"""
Teste específico para verificar problemas de sessão
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoProject.settings')
django.setup()

from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.test import Client
from django.contrib.auth import authenticate, login
from django.utils import timezone
import json

def test_session_persistence():
    """Testa se a sessão persiste após login"""
    print("=== TESTE DE PERSISTÊNCIA DE SESSÃO ===")
    
    # Verificar usuários existentes
    users = User.objects.all()
    print(f"Usuários no banco: {users.count()}")
    
    if not users.exists():
        print("Nenhum usuário para testar")
        return
    
    user = users.first()
    print(f"Testando com usuário: {user.username}")
    
    # Test client
    client = Client()
    
    # 1. Verificar homepage sem login
    print("\n1. Acessando homepage sem login:")
    response = client.get('/')
    print(f"   Status: {response.status_code}")
    print(f"   Usuário autenticado: {response.wsgi_request.user.is_authenticated}")
    
    # 2. Tentar login
    print("\n2. Tentando login:")
    login_data = {
        'email': user.email,
        'password': 'test123'  # Assume que a senha é test123
    }
    
    response = client.post('/auth/login/', login_data, follow=True)
    print(f"   Status final: {response.status_code}")
    print(f"   URL final: {response.request['PATH_INFO']}")
    
    # 3. Verificar se há sessão ativa
    print("\n3. Verificando sessões ativas:")
    sessions = Session.objects.filter(expire_date__gt=timezone.now())
    print(f"   Sessões ativas: {sessions.count()}")
    
    for session in sessions:
        data = session.get_decoded()
        user_id = data.get('_auth_user_id')
        if user_id:
            print(f"   Sessão encontrada para user_id: {user_id}")
    
    # 4. Acessar homepage novamente
    print("\n4. Acessando homepage após login:")
    response = client.get('/')
    print(f"   Status: {response.status_code}")
    print(f"   Usuário autenticado: {response.wsgi_request.user.is_authenticated}")
    if response.wsgi_request.user.is_authenticated:
        print(f"   Usuário: {response.wsgi_request.user.username}")

def test_force_login():
    """Testa force login para comparação"""
    print("\n=== TESTE DE FORCE LOGIN ===")
    
    client = Client()
    
    # Acessar force login
    response = client.get('/force-login/', follow=True)
    print(f"Status: {response.status_code}")
    print(f"URL final: {response.request['PATH_INFO']}")
    
    # Verificar se está autenticado agora
    response = client.get('/')
    print(f"Autenticado após force login: {response.wsgi_request.user.is_authenticated}")
    if response.wsgi_request.user.is_authenticated:
        print(f"Usuário: {response.wsgi_request.user.username}")

def show_session_config():
    """Mostra configurações de sessão"""
    print("\n=== CONFIGURAÇÕES DE SESSÃO ===")
    from django.conf import settings
    
    session_configs = [
        'SESSION_ENGINE',
        'SESSION_COOKIE_NAME', 
        'SESSION_COOKIE_AGE',
        'SESSION_COOKIE_SECURE',
        'SESSION_COOKIE_HTTPONLY',
        'SESSION_COOKIE_SAMESITE',
        'SESSION_SAVE_EVERY_REQUEST',
        'SESSION_EXPIRE_AT_BROWSER_CLOSE'
    ]
    
    for config in session_configs:
        value = getattr(settings, config, 'NÃO DEFINIDO')
        print(f"{config}: {value}")

if __name__ == "__main__":
    show_session_config()
    test_session_persistence()
    test_force_login()