#!/usr/bin/env python
"""
Script para testar a autenticação do Supabase e identificar o erro "Invalid API key"
"""
import os
import sys
import django
from pathlib import Path

# Configurar Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoProject.settings')
django.setup()

from supabase import create_client
from django.conf import settings

def test_supabase_keys():
    """Testa se as chaves do Supabase são válidas"""
    
    print("=" * 50)
    print("TESTE DE AUTENTICAÇÃO SUPABASE")
    print("=" * 50)
    
    # Verificar se as variáveis estão definidas
    print("\n1. Verificando variáveis de ambiente:")
    print(f"   SUPABASE_URL: {'✓' if settings.SUPABASE_URL else '✗'} {settings.SUPABASE_URL[:40]}..." if settings.SUPABASE_URL else "   SUPABASE_URL: ✗ Não definida")
    print(f"   SUPABASE_ANON_KEY: {'✓' if settings.SUPABASE_ANON_KEY else '✗'} {settings.SUPABASE_ANON_KEY[:40]}..." if settings.SUPABASE_ANON_KEY else "   SUPABASE_ANON_KEY: ✗ Não definida")
    print(f"   SUPABASE_SERVICE_ROLE_KEY: {'✓' if settings.SUPABASE_SERVICE_ROLE_KEY else '✗'} {settings.SUPABASE_SERVICE_ROLE_KEY[:40]}..." if settings.SUPABASE_SERVICE_ROLE_KEY else "   SUPABASE_SERVICE_ROLE_KEY: ✗ Não definida")
    
    # Testar conexão com anon key
    print("\n2. Testando conexão com ANON KEY:")
    try:
        client = create_client(settings.SUPABASE_URL, settings.SUPABASE_ANON_KEY)
        # Tentar fazer uma operação simples
        response = client.table('produtos_produto').select('*').limit(1).execute()
        print("   ✓ Conexão bem-sucedida com ANON KEY")
        print(f"   ✓ Teste de query: {len(response.data)} registro(s) retornados")
    except Exception as e:
        print(f"   ✗ Erro ao conectar com ANON KEY: {e}")
        print(f"   Tipo do erro: {type(e).__name__}")
    
    # Testar conexão com service role key
    print("\n3. Testando conexão com SERVICE ROLE KEY:")
    try:
        admin_client = create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_ROLE_KEY)
        # Tentar fazer uma operação simples
        response = admin_client.table('produtos_produto').select('*').limit(1).execute()
        print("   ✓ Conexão bem-sucedida com SERVICE ROLE KEY")
        print(f"   ✓ Teste de query: {len(response.data)} registro(s) retornados")
    except Exception as e:
        print(f"   ✗ Erro ao conectar com SERVICE ROLE KEY: {e}")
        print(f"   Tipo do erro: {type(e).__name__}")
    
    # Testar autenticação de usuário
    print("\n4. Testando autenticação de usuário:")
    try:
        client = create_client(settings.SUPABASE_URL, settings.SUPABASE_ANON_KEY)
        # Tentar fazer login com credenciais de teste
        test_email = "Axxycorporation@gmail.com"
        test_password = "admin8477thygas"
        
        response = client.auth.sign_in_with_password({
            "email": test_email,
            "password": test_password
        })
        
        if response.user:
            print(f"   ✓ Login bem-sucedido para {test_email}")
            print(f"   ✓ User ID: {response.user.id}")
            print(f"   ✓ Access Token: {response.session.access_token[:40]}...")
        else:
            print(f"   ✗ Falha no login - resposta vazia")
            
    except Exception as e:
        print(f"   ✗ Erro ao fazer login: {e}")
        print(f"   Tipo do erro: {type(e).__name__}")
        
        # Se for erro de API, tentar extrair mais detalhes
        if hasattr(e, 'response'):
            print(f"   Status Code: {getattr(e.response, 'status_code', 'N/A')}")
            print(f"   Response: {getattr(e.response, 'text', 'N/A')}")
    
    print("\n" + "=" * 50)
    print("TESTE CONCLUÍDO")
    print("=" * 50)

if __name__ == "__main__":
    test_supabase_keys()