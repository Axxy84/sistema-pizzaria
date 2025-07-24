#!/usr/bin/env python
"""
Script para testar autenticação usando SQLite temporariamente
"""

import os
import django
import sys

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoProject.settings')

# Forçar uso do SQLite
os.environ['USE_SUPABASE_DB'] = 'False'

django.setup()

from django.contrib.auth import authenticate
from django.test import Client

def test_auth_sqlite():
    print("=== TESTE DE AUTENTICAÇÃO (SQLite) ===\n")
    
    # 1. Criar/atualizar usuário admin
    print("1. Criando/atualizando usuário admin@pizzaria.com:")
    try:
        user = get_user_model().objects.get(username='admin@pizzaria.com')
        print(f"   - Usuário já existe: {user.username}")
    except User.DoesNotExist:
        user = get_user_model().objects.create_user(
            username='admin@pizzaria.com',
            email='admin@pizzaria.com',
            password='admin8477thygas'
        )
        print(f"   - Usuário criado: {user.username}")
    
    # Garantir que está ativo
    user.is_active = True
    user.is_staff = True
    user.save()
    print(f"   - Ativo: {user.is_active}, Staff: {user.is_staff}")
    print()
    
    # 2. Testar autenticação
    print("2. Testando autenticação:")
    auth_user = authenticate(username='admin@pizzaria.com', password='admin8477thygas')
    if auth_user:
        print(f"   ✓ Autenticação bem-sucedida: {auth_user.username}")
    else:
        print("   ✗ Falha na autenticação")
    print()
    
    # 3. Testar login via Client
    print("3. Testando login via Client Django:")
    client = Client()
    
    # Testar login
    logged_in = client.login(username='admin@pizzaria.com', password='admin8477thygas')
    if logged_in:
        print("   ✓ Login via client.login() bem-sucedido")
    else:
        print("   ✗ Login via client.login() falhou")
    
    # Verificar se está autenticado
    response = client.get('/')
    if response.wsgi_request.user.is_authenticated:
        print(f"   ✓ Usuário autenticado na home: {response.wsgi_request.user.username}")
    else:
        print("   ✗ Usuário não autenticado na home")
    print()
    
    # 4. Testar login via POST
    print("4. Testando login via POST /auth/login/:")
    client2 = Client()
    
    login_data = {
        'email': 'admin@pizzaria.com',
        'password': 'admin8477thygas'
    }
    
    response = client2.post('/auth/login/', data=login_data, follow=True)
    print(f"   - Status code: {response.status_code}")
    
    if response.wsgi_request.user.is_authenticated:
        print(f"   ✓ Login POST bem-sucedido: {response.wsgi_request.user.username}")
    else:
        print("   ✗ Login POST falhou")
        
        # Verificar mensagens de erro
        if hasattr(response, 'context') and response.context:
            if 'error' in response.context:
                print(f"   - Erro: {response.context['error']}")
    
    # Verificar redirecionamentos
    if response.redirect_chain:
        print(f"   - Redirecionamentos: {response.redirect_chain}")
    print()
    
    print("5. Informações de debug:")
    from django.conf import settings
    print(f"   - USE_SUPABASE_DB: {os.environ.get('USE_SUPABASE_DB', 'não definido')}")
    print(f"   - AUTHENTICATION_BACKENDS: {settings.AUTHENTICATION_BACKENDS}")
    print(f"   - Banco atual: SQLite (forçado)")

if __name__ == '__main__':
    test_auth_sqlite()