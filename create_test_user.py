#!/usr/bin/env python
"""
Criar usuário de teste com senha
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoProject.settings')
django.setup()

from django.contrib.auth.models import User

def create_test_user():
    """Cria usuário de teste com senha"""
    print("=== CRIANDO USUÁRIO DE TESTE ===")
    
    # Verificar se já existe
    username = 'test@test.com'
    try:
        user = User.objects.get(username=username)
        print(f"Usuário {username} já existe. Atualizando senha...")
        user.set_password('test123')
        user.save()
    except User.DoesNotExist:
        print(f"Criando usuário {username}...")
        user = User.objects.create_user(
            username=username,
            email=username,
            password='test123',
            first_name='Test',
            last_name='User'
        )
    
    print(f"Usuário: {user.username}")
    print(f"Email: {user.email}")
    print(f"ID: {user.id}")
    print(f"Tem senha? {user.has_usable_password()}")
    
    # Testar autenticação
    from django.contrib.auth import authenticate
    auth_user = authenticate(username=username, password='test123')
    print(f"Authenticate funcionou? {auth_user is not None}")
    
    return user

if __name__ == "__main__":
    create_test_user()