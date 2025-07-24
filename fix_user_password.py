#!/usr/bin/env python
"""
Script para criar um usuário Django com senha local para teste
"""
import os
import sys
import django

# Adiciona o projeto ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoProject.settings')
django.setup()


def create_test_user():
    """Cria usuário de teste com senha Django"""
    email = 'Axxycorporation@gmail.com'
    password = 'A1'
    
    # Buscar usuário existente
    user = get_user_model().objects.filter(username=email).first()
    
    if user:
        print(f"Usuário {email} já existe (ID: {user.id})")
        print(f"Tem senha utilizável? {user.has_usable_password()}")
        
        # Definir senha Django
        user.set_password(password)
        user.save()
        print(f"✅ Senha Django definida para o usuário!")
        
        # Testar autenticação
        from django.contrib.auth import authenticate
        test_user = authenticate(username=email, password=password)
        if test_user:
            print(f"✅ Autenticação Django funcionando!")
        else:
            print(f"❌ Falha na autenticação Django")
    else:
        # Criar novo usuário
        user = get_user_model().objects.create_user(
            username=email,
            email=email,
            password=password
        )
        print(f"✅ Usuário {email} criado com sucesso (ID: {user.id})")
    
    # Criar usuário admin para teste também
    admin_email = 'admin@pizzaria.com'
    admin_password = 'admin123'
    
    admin_user = get_user_model().objects.filter(username=admin_email).first()
    if not admin_user:
        admin_user = get_user_model().objects.create_superuser(
            username=admin_email,
            email=admin_email,
            password=admin_password
        )
        print(f"\n✅ Superusuário {admin_email} criado!")
        print(f"   Senha: {admin_password}")
    else:
        admin_user.set_password(admin_password)
        admin_user.is_superuser = True
        admin_user.is_staff = True
        admin_user.save()
        print(f"\n✅ Superusuário {admin_email} atualizado!")
    
    print("\n--- USUÁRIOS DISPONÍVEIS PARA TESTE ---")
    print(f"1. Email: {email}")
    print(f"   Senha: {password}")
    print(f"\n2. Email: {admin_email}")
    print(f"   Senha: {admin_password}")
    print("\nUse estes dados para fazer login!")

if __name__ == "__main__":
    create_test_user()