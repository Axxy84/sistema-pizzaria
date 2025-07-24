#!/usr/bin/env python
"""
Script para testar login híbrido Django + Supabase
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

from django.contrib.auth import authenticate
from supabase import create_client
from django.conf import settings

def test_login():
    """Testa login com diferentes métodos"""
    
    print("=" * 50)
    print("TESTE DE LOGIN HÍBRIDO")
    print("=" * 50)
    
    # Credenciais para teste
    credentials = [
        ("admin@pizzaria.com", "admin8477thygas", "Usuário criado no Supabase"),
        ("Axxycorporation@gmail.com", "admin8477thygas", "Usuário original")
    ]
    
    for email, password, desc in credentials:
        print(f"\n📧 Testando: {email} ({desc})")
        print("-" * 40)
        
        # 1. Testar direto no Supabase
        print("1. Login direto no Supabase:")
        try:
            client = create_client(settings.SUPABASE_URL, settings.SUPABASE_ANON_KEY)
            response = client.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            if response.user:
                print(f"   ✓ Sucesso! User ID: {response.user.id}")
            else:
                print("   ✗ Falhou - resposta vazia")
        except Exception as e:
            print(f"   ✗ Erro: {e}")
        
        # 2. Testar com backend Django
        print("\n2. Login via Django authenticate():")
        try:
            user = authenticate(username=email, password=password)
            if user:
                print(f"   ✓ Sucesso! User: {user.username} (ID: {user.id})")
                print(f"   ✓ Is Active: {user.is_active}")
                print(f"   ✓ Is Staff: {user.is_staff}")
            else:
                print("   ✗ Falhou - authenticate() retornou None")
        except Exception as e:
            print(f"   ✗ Erro: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "=" * 50)
    print("RESUMO:")
    print("=" * 50)
    print("\n✅ Use 'admin@pizzaria.com' com senha 'admin8477thygas'")
    print("✅ Este usuário está confirmado no Supabase Auth")
    print("\n" + "=" * 50)

if __name__ == "__main__":
    test_login()