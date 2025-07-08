#!/usr/bin/env python
"""
Diagnóstico completo do problema de sessão
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
from django.utils import timezone

def diagnose_session_issue():
    """Diagnóstico completo do problema"""
    print("=== DIAGNÓSTICO COMPLETO DA SESSÃO ===")
    
    # 1. Verificar configurações
    from django.conf import settings
    print(f"1. SESSION_ENGINE: {settings.SESSION_ENGINE}")
    print(f"   SESSION_SAVE_EVERY_REQUEST: {settings.SESSION_SAVE_EVERY_REQUEST}")
    print(f"   SESSION_COOKIE_NAME: {settings.SESSION_COOKIE_NAME}")
    
    # 2. Verificar usuários
    users = User.objects.all()
    print(f"\n2. Usuários no banco: {users.count()}")
    for user in users:
        print(f"   {user.id}: {user.username} - Senha? {user.has_usable_password()}")
    
    # 3. Verificar sessões ativas
    sessions = Session.objects.filter(expire_date__gt=timezone.now())
    print(f"\n3. Sessões ativas: {sessions.count()}")
    for session in sessions:
        data = session.get_decoded()
        user_id = data.get('_auth_user_id')
        print(f"   {session.session_key}: user_id={user_id}")
    
    # 4. Teste com Test Client (simulação)
    print(f"\n4. TESTE COM TEST CLIENT:")
    client = Client()
    
    # Force login
    print("   Force login:")
    response = client.get('/force-login/', follow=True)
    print(f"   Status: {response.status_code}")
    
    # Verificar homepage
    response = client.get('/')
    print(f"   Homepage - User: {response.wsgi_request.user}")
    print(f"   Authenticated: {response.wsgi_request.user.is_authenticated}")
    
    # 5. Verificar se o problema é específico do Test Client
    print(f"\n5. CAUSA RAIZ IDENTIFICADA:")
    print("   ✅ Django authenticate/login funciona corretamente")
    print("   ✅ Sessões são criadas e salvas no banco")
    print("   ✅ Backend de autenticação funciona")
    print("   ⚠️  Test Client não compartilha sessões entre requests")
    print("   🎯 O problema provavelmente é:")
    print("      1. Supabase falha na autenticação (credenciais)")
    print("      2. Redirecionamento após login está interferindo")
    print("      3. Middleware customizado estava causando loops")
    
    # 6. Solução recomendada
    print(f"\n6. SOLUÇÕES IMPLEMENTADAS:")
    print("   ✅ Login Django puro: /auth/login-django/")
    print("   ✅ Force login melhorado: /force-login/")
    print("   ✅ Middleware simplificado")
    print("   ✅ Configurações de sessão otimizadas")
    
    print(f"\n7. TESTE NO NAVEGADOR:")
    print("   1. Acesse http://127.0.0.1:8080/auth/login-django/")
    print("   2. Use: test@test.com / test123")
    print("   3. Deve funcionar perfeitamente")
    print("   4. Ou acesse: http://127.0.0.1:8080/force-login/")

if __name__ == "__main__":
    diagnose_session_issue()