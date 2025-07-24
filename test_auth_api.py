#!/usr/bin/env python
"""
Script para testar a API de autenticação
"""

import os
import django
import sys

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoProject.settings')
django.setup()

from django.contrib.auth import authenticate, login
from django.test import RequestFactory, Client
from apps.authentication.backends import SupabaseBackend
import json

def test_authentication():
    print("=== TESTE DE AUTENTICAÇÃO ===\n")
    
    # 1. Verificar usuários existentes
    print("1. Usuários no banco Django:")
    users = get_user_model().objects.all()
    for user in users:
        print(f"   - {user.username} (email: {user.email}, ativo: {user.is_active})")
    print()
    
    # 2. Testar autenticação direta
    print("2. Testando autenticação com admin@pizzaria.com:")
    user = authenticate(username='admin@pizzaria.com', password='admin8477thygas')
    if user:
        print(f"   ✓ Autenticação bem-sucedida: {user.username}")
        print(f"   - É staff: {user.is_staff}")
        print(f"   - É superuser: {user.is_superuser}")
        print(f"   - Está ativo: {user.is_active}")
    else:
        print("   ✗ Falha na autenticação")
    print()
    
    # 3. Testar login via API
    print("3. Testando login via endpoint /auth/login/:")
    client = Client()
    
    # Fazer GET primeiro para obter CSRF token
    response = client.get('/auth/login/')
    print(f"   - GET /auth/login/: {response.status_code}")
    
    # Fazer POST com credenciais
    login_data = {
        'email': 'admin@pizzaria.com',
        'password': 'admin8477thygas'
    }
    response = client.post('/auth/login/', data=login_data, follow=True)
    print(f"   - POST /auth/login/: {response.status_code}")
    
    # Verificar se está autenticado
    if response.wsgi_request.user.is_authenticated:
        print(f"   ✓ Login bem-sucedido: {response.wsgi_request.user.username}")
    else:
        print("   ✗ Login falhou - usuário não autenticado")
        
    # Verificar redirecionamento
    if response.redirect_chain:
        print(f"   - Redirecionamentos: {response.redirect_chain}")
    print()
    
    # 4. Verificar sessão
    print("4. Verificando sessão:")
    response = client.get('/')
    if response.wsgi_request.user.is_authenticated:
        print(f"   ✓ Sessão mantida: {response.wsgi_request.user.username}")
    else:
        print("   ✗ Sessão não mantida - usuário anônimo")
    print()
    
    # 5. Testar backend Supabase diretamente
    print("5. Testando backend Supabase diretamente:")
    backend = SupabaseBackend()
    try:
        # Criar request fake
        request = RequestFactory().post('/auth/login/')
        user = backend.authenticate(request, username='admin@pizzaria.com', password='admin8477thygas')
        if user:
            print(f"   ✓ Backend Supabase funcionando: {user.username}")
        else:
            print("   ✗ Backend Supabase retornou None")
    except Exception as e:
        print(f"   ✗ Erro no backend Supabase: {e}")
    print()
    
    # 6. Verificar configurações
    print("6. Verificações de configuração:")
    from django.conf import settings
    print(f"   - SESSION_ENGINE: {settings.SESSION_ENGINE}")
    print(f"   - SESSION_COOKIE_NAME: {settings.SESSION_COOKIE_NAME}")
    print(f"   - SESSION_COOKIE_AGE: {settings.SESSION_COOKIE_AGE}")
    print(f"   - SESSION_SAVE_EVERY_REQUEST: {getattr(settings, 'SESSION_SAVE_EVERY_REQUEST', False)}")
    print(f"   - AUTHENTICATION_BACKENDS: {settings.AUTHENTICATION_BACKENDS}")
    print()

if __name__ == '__main__':
    test_authentication()