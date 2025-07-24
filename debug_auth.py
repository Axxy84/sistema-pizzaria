#!/usr/bin/env python
"""
Debug direto da autenticação Django
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoProject.settings')
django.setup()

from django.contrib.auth import authenticate, login
from django.test import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.auth.middleware import AuthenticationMiddleware

def debug_authentication():
    """Debug direto da autenticação"""
    print("=== DEBUG AUTENTICAÇÃO DJANGO ===")
    
    # Verificar usuários
    users = get_user_model().objects.all()
    print(f"Usuários no banco: {users.count()}")
    
    if not users.exists():
        print("Criando usuário de teste...")
        user = get_user_model().objects.create_user(
            username='test@test.com',
            email='test@test.com',
            password='test123'
        )
        print(f"Usuário criado: {user.username}")
    else:
        user = users.first()
        print(f"Usando usuário existente: {user.username}")
    
    # Teste 1: authenticate() direto
    print(f"\n1. Teste authenticate() com ModelBackend:")
    auth_user = authenticate(username=user.username, password='test123')
    print(f"   Resultado: {auth_user}")
    
    # Teste 2: Criar request factory
    print(f"\n2. Teste com RequestFactory:")
    factory = RequestFactory()
    request = factory.get('/')
    
    # Adicionar sessão
    middleware = SessionMiddleware(lambda r: None)
    middleware.process_request(request)
    request.session.save()
    
    # Adicionar auth middleware
    auth_middleware = AuthenticationMiddleware(lambda r: None)
    auth_middleware.process_request(request)
    
    print(f"   Usuário antes do login: {request.user}")
    print(f"   Autenticado antes: {request.user.is_authenticated}")
    
    # Fazer login direto
    if auth_user:
        login(request, auth_user)
        print(f"   Usuário após login: {request.user}")
        print(f"   Autenticado após: {request.user.is_authenticated}")
        print(f"   Session key: {request.session.session_key}")
        print(f"   Auth user ID in session: {request.session.get('_auth_user_id')}")
    
    # Teste 3: Verificar backend
    print(f"\n3. Teste do backend:")
    from apps.authentication.backends import SupabaseBackend
    backend = SupabaseBackend()
    
    # get_user direto
    if users.exists():
        test_user = backend.get_user(user.id)
        print(f"   Backend get_user({user.id}): {test_user}")

if __name__ == "__main__":
    debug_authentication()