#!/usr/bin/env python
"""
Script para criar usuário admin no Django sincronizado com Supabase
"""
import os
import sys
import django
from pathlib import Path

# Configurar Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoProject.settings')

# Sistema agora usa apenas Supabase

django.setup()


def create_admin_user():
    """Cria usuário admin no Django"""
    
    print("=" * 50)
    print("CRIANDO USUÁRIO ADMIN NO DJANGO")
    print("=" * 50)
    
    email = 'admin@pizzaria.com'
    password = 'admin8477thygas'
    
    try:
        user, created = get_user_model().objects.get_or_create(
            username=email,
            defaults={
                'email': email,
                'first_name': 'Admin',
                'last_name': 'Pizzaria',
                'is_staff': True,
                'is_superuser': True,
                'is_active': True
            }
        )
        
        # Sempre atualizar a senha
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save()
        
        if created:
            print(f"\n✓ Usuário {email} criado com sucesso!")
        else:
            print(f"\n✓ Usuário {email} já existia e foi atualizado!")
            
        print(f"\n📧 Email: {email}")
        print(f"🔑 Senha: {password}")
        print(f"👤 ID: {user.id}")
        print(f"✅ Staff: {user.is_staff}")
        print(f"✅ Superuser: {user.is_superuser}")
        print(f"✅ Ativo: {user.is_active}")
        
        print("\n✅ PRONTO! Você pode fazer login com estas credenciais:")
        print(f"   - No Django Admin: http://127.0.0.1:8000/admin/")
        print(f"   - No sistema: http://127.0.0.1:8000/auth/login/")
        
    except Exception as e:
        print(f"\n✗ Erro ao criar usuário: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 50)

if __name__ == "__main__":
    create_admin_user()