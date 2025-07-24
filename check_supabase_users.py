#!/usr/bin/env python
"""
Script para verificar usuários no Supabase Auth
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

def check_users():
    """Verifica usuários no Django e tenta criar/resetar no Supabase"""
    
    print("=" * 50)
    print("VERIFICAÇÃO DE USUÁRIOS")
    print("=" * 50)
    
    # Listar usuários Django
    print("\n1. Usuários no Django:")
    django_users = get_user_model().objects.all()
    for user in django_users:
        print(f"   - {user.username} (email: {user.email}, id: {user.id})")
    
    # Conectar ao Supabase com service role (admin)
    print("\n2. Tentando listar usuários no Supabase Auth:")
    try:
        admin_client = create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_ROLE_KEY)
        
        # Listar usuários (requer service_role key)
        # NOTA: A API do Supabase Auth não tem um endpoint direto para listar usuários
        # Vamos tentar criar um novo usuário ou resetar a senha
        
        print("\n3. Criando/Atualizando usuário de teste no Supabase:")
        test_email = "Axxycorporation@gmail.com"
        test_password = "admin8477thygas"
        
        try:
            # Tentar criar usuário
            response = admin_client.auth.admin.create_user({
                "email": test_email,
                "password": test_password,
                "email_confirm": True  # Auto-confirmar email
            })
            print(f"   ✓ Usuário criado com sucesso: {response.user.id}")
        except Exception as create_error:
            print(f"   ⚠ Erro ao criar usuário (pode já existir): {create_error}")
            
            # Se falhou, tentar atualizar a senha
            try:
                # Buscar usuário por email primeiro
                print("\n4. Tentando atualizar senha do usuário existente:")
                # Vamos usar um método alternativo
                response = admin_client.auth.admin.update_user_by_id(
                    user_id="",  # Precisamos do ID do usuário
                    attributes={
                        "password": test_password
                    }
                )
                print(f"   ✓ Senha atualizada com sucesso")
            except Exception as update_error:
                print(f"   ✗ Erro ao atualizar senha: {update_error}")
        
        # Testar login após criar/atualizar
        print("\n5. Testando login após criar/atualizar:")
        try:
            client = create_client(settings.SUPABASE_URL, settings.SUPABASE_ANON_KEY)
            response = client.auth.sign_in_with_password({
                "email": test_email,
                "password": test_password
            })
            
            if response.user:
                print(f"   ✓ Login bem-sucedido!")
                print(f"   ✓ User ID: {response.user.id}")
                print(f"   ✓ Email: {response.user.email}")
            else:
                print(f"   ✗ Login falhou - resposta vazia")
                
        except Exception as login_error:
            print(f"   ✗ Erro no login: {login_error}")
            
    except Exception as e:
        print(f"   ✗ Erro geral: {e}")
    
    print("\n" + "=" * 50)

if __name__ == "__main__":
    check_users()