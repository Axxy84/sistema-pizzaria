#!/usr/bin/env python
"""
Script para criar usuário diretamente no Supabase Auth
"""
import os
from dotenv import load_dotenv
from supabase import create_client

# Carregar variáveis de ambiente
load_dotenv()

def create_user():
    """Cria um usuário no Supabase Auth"""
    
    print("=" * 50)
    print("CRIANDO USUÁRIO NO SUPABASE AUTH")
    print("=" * 50)
    
    # Pegar variáveis de ambiente
    url = os.getenv('SUPABASE_URL')
    service_key = os.getenv('SUPABASE_SERVICE_ROLE_KEY')
    anon_key = os.getenv('SUPABASE_ANON_KEY')
    
    print(f"\nURL: {url}")
    print(f"Service Key: {service_key[:40]}...")
    print(f"Anon Key: {anon_key[:40]}...")
    
    # Conectar com service role para criar usuário
    print("\n1. Conectando ao Supabase com Service Role...")
    try:
        admin_client = create_client(url, service_key)
        print("   ✓ Conectado com sucesso")
    except Exception as e:
        print(f"   ✗ Erro na conexão: {e}")
        return
    
    # Dados do usuário
    test_email = "Axxycorporation@gmail.com"
    test_password = "admin8477thygas"
    
    # Tentar criar usuário
    print(f"\n2. Criando usuário {test_email}...")
    try:
        response = admin_client.auth.admin.create_user({
            "email": test_email,
            "password": test_password,
            "email_confirm": True,
            "user_metadata": {
                "first_name": "Admin",
                "last_name": "Pizzaria"
            }
        })
        print(f"   ✓ Usuário criado com sucesso!")
        print(f"   ID: {response.user.id}")
        print(f"   Email: {response.user.email}")
    except Exception as e:
        error_msg = str(e)
        if "already been registered" in error_msg:
            print(f"   ⚠ Usuário já existe. Tentando resetar senha...")
            
            # Se usuário existe, vamos tentar fazer login direto para confirmar
            print("\n3. Tentando fazer login com credenciais atuais...")
            try:
                client = create_client(url, anon_key)
                response = client.auth.sign_in_with_password({
                    "email": test_email,
                    "password": test_password
                })
                print(f"   ✓ Login bem-sucedido! As credenciais estão corretas.")
                print(f"   ID: {response.user.id}")
                return
            except Exception as login_error:
                print(f"   ✗ Login falhou: {login_error}")
                print("\n4. Enviando email de reset de senha...")
                try:
                    # Enviar email de reset
                    client = create_client(url, anon_key)
                    response = client.auth.reset_password_email(test_email)
                    print(f"   ✓ Email de reset enviado para {test_email}")
                    print("   Por favor, verifique seu email para resetar a senha.")
                except Exception as reset_error:
                    print(f"   ✗ Erro ao enviar email: {reset_error}")
        else:
            print(f"   ✗ Erro ao criar usuário: {e}")
    
    # Testar login após criar
    print("\n5. Testando login com o usuário criado...")
    try:
        client = create_client(url, anon_key)
        response = client.auth.sign_in_with_password({
            "email": test_email,
            "password": test_password
        })
        print(f"   ✓ Login bem-sucedido!")
        print(f"   Access Token: {response.session.access_token[:40]}...")
    except Exception as e:
        print(f"   ✗ Erro no login: {e}")
    
    print("\n" + "=" * 50)

if __name__ == "__main__":
    create_user()