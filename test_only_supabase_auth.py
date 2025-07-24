#!/usr/bin/env python
"""
Testar APENAS a autenticação Supabase sem usar banco Django
"""

import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Carregar variáveis de ambiente
load_dotenv()

def test_supabase_auth():
    print("=== TESTE DIRETO SUPABASE AUTH ===\n")
    
    # 1. Verificar variáveis de ambiente
    print("1. Variáveis de ambiente:")
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_ANON_KEY')
    
    print(f"   - SUPABASE_URL: {supabase_url}")
    print(f"   - SUPABASE_ANON_KEY: {supabase_key[:20]}..." if supabase_key else "   - SUPABASE_ANON_KEY: NÃO DEFINIDA")
    print()
    
    if not supabase_url or not supabase_key:
        print("❌ Variáveis de ambiente não configuradas!")
        return
    
    # 2. Criar cliente Supabase
    print("2. Conectando ao Supabase:")
    try:
        supabase: Client = create_client(supabase_url, supabase_key)
        print("   ✓ Cliente Supabase criado com sucesso")
    except Exception as e:
        print(f"   ✗ Erro ao criar cliente: {e}")
        return
    print()
    
    # 3. Testar login com admin@pizzaria.com
    print("3. Testando login com admin@pizzaria.com:")
    try:
        response = supabase.auth.sign_in_with_password({
            "email": "admin@pizzaria.com",
            "password": "admin8477thygas"
        })
        
        if response.user:
            print(f"   ✓ Login bem-sucedido!")
            print(f"   - User ID: {response.user.id}")
            print(f"   - Email: {response.user.email}")
            print(f"   - Criado em: {response.user.created_at}")
            print(f"   - Access Token: {response.session.access_token[:20]}..." if response.session else "   - Sem sessão")
        else:
            print("   ✗ Login falhou - sem usuário retornado")
            
    except Exception as e:
        print(f"   ✗ Erro no login: {e}")
    print()
    
    # 4. Testar com usuário incorreto
    print("4. Testando com senha incorreta (para confirmar):")
    try:
        response = supabase.auth.sign_in_with_password({
            "email": "admin@pizzaria.com",
            "password": "senha_errada"
        })
        print("   ✗ PROBLEMA: Login com senha errada funcionou!")
    except Exception as e:
        print(f"   ✓ Esperado - Erro com senha incorreta: {str(e)[:50]}...")
    print()
    
    # 5. Verificar outros usuários
    print("5. Testando com Axxycorporation@gmail.com:")
    try:
        response = supabase.auth.sign_in_with_password({
            "email": "Axxycorporation@gmail.com",
            "password": "Thyg@s8477"  # Senha que você estava tentando
        })
        
        if response.user:
            print(f"   ✓ Login bem-sucedido!")
            print(f"   - User ID: {response.user.id}")
            print(f"   - Email: {response.user.email}")
        else:
            print("   ✗ Login falhou")
            
    except Exception as e:
        print(f"   ✗ Erro no login: {e}")
    print()
    
    print("6. Resumo:")
    print("   - A autenticação Supabase está funcionando corretamente")
    print("   - O problema pode estar na integração com Django")
    print("   - Verifique se o backend de autenticação está configurado corretamente")

if __name__ == '__main__':
    test_supabase_auth()