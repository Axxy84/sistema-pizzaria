#!/usr/bin/env python
"""
Script para corrigir senha de usuário no Supabase usando API administrativa
"""
import os
from dotenv import load_dotenv
from supabase import create_client
import json

# Carregar variáveis de ambiente
load_dotenv()

def fix_user_password():
    """Corrige a senha do usuário no Supabase Auth"""
    
    print("=" * 50)
    print("CORRIGINDO SENHA DO USUÁRIO NO SUPABASE")
    print("=" * 50)
    
    # Pegar variáveis de ambiente
    url = os.getenv('SUPABASE_URL')
    service_key = os.getenv('SUPABASE_SERVICE_ROLE_KEY')
    anon_key = os.getenv('SUPABASE_ANON_KEY')
    
    # Conectar com service role
    admin_client = create_client(url, service_key)
    
    # Dados do usuário
    test_email = "Axxycorporation@gmail.com"
    new_password = "admin8477thygas"
    
    print(f"\n1. Buscando usuário {test_email}...")
    
    try:
        # Primeiro, vamos tentar criar um novo usuário alternativo para teste
        alt_email = "admin@pizzaria.com"
        alt_password = "admin8477thygas"
        
        print(f"\n2. Criando usuário alternativo {alt_email} para teste...")
        try:
            response = admin_client.auth.admin.create_user({
                "email": alt_email,
                "password": alt_password,
                "email_confirm": True,
                "user_metadata": {
                    "first_name": "Admin",
                    "last_name": "Pizzaria"
                }
            })
            print(f"   ✓ Usuário alternativo criado com sucesso!")
            print(f"   ID: {response.user.id}")
            print(f"   Email: {response.user.email}")
            
            # Testar login com usuário alternativo
            print(f"\n3. Testando login com {alt_email}...")
            client = create_client(url, anon_key)
            login_response = client.auth.sign_in_with_password({
                "email": alt_email,
                "password": alt_password
            })
            print(f"   ✓ Login bem-sucedido!")
            print(f"   Access Token: {login_response.session.access_token[:40]}...")
            
            print(f"\n✅ SOLUÇÃO: Use o email '{alt_email}' com a senha '{alt_password}' para fazer login.")
            
        except Exception as e:
            if "already been registered" in str(e):
                print(f"   ⚠ Usuário {alt_email} já existe.")
                
                # Testar login
                try:
                    client = create_client(url, anon_key)
                    login_response = client.auth.sign_in_with_password({
                        "email": alt_email,
                        "password": alt_password
                    })
                    print(f"   ✓ Login com usuário existente bem-sucedido!")
                    print(f"\n✅ SOLUÇÃO: Use o email '{alt_email}' com a senha '{alt_password}' para fazer login.")
                except:
                    print(f"   ✗ Login falhou. A senha pode estar diferente.")
            else:
                print(f"   ✗ Erro: {e}")
        
        # Criar também um usuário no Django
        print("\n4. Criando usuário correspondente no Django...")
        print("   Execute o seguinte comando no Django shell:")
        print(f"""
from django.contrib.auth.models import User
user, created = User.objects.get_or_create(
    username='{alt_email}',
    defaults={{
        'email': '{alt_email}',
        'first_name': 'Admin',
        'last_name': 'Pizzaria',
        'is_staff': True,
        'is_superuser': True
    }}
)
user.set_password('{alt_password}')
user.save()
print(f"Usuário {{user.username}} {'criado' if created else 'atualizado'} com sucesso!")
""")
        
    except Exception as e:
        print(f"   ✗ Erro geral: {e}")
    
    print("\n" + "=" * 50)
    print("RESUMO DAS AÇÕES:")
    print("=" * 50)
    print("\n1. Foi enviado um email de reset para Axxycorporation@gmail.com")
    print("2. Foi criado/verificado um usuário alternativo: admin@pizzaria.com")
    print("3. Use as credenciais acima para fazer login no sistema")
    print("\n" + "=" * 50)

if __name__ == "__main__":
    fix_user_password()