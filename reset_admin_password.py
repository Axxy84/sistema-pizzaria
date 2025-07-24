#\!/usr/bin/env python
"""
Script para redefinir a senha do usuário admin
"""
import os
import django
import sys

# Adiciona o diretório do projeto ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Configura o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoProject.settings')
django.setup()


def reset_admin_password():
    """Redefine a senha do usuário admin"""
    print("=== Redefinição de Senha do Admin ===\n")
    
    # Buscar usuário admin (ID 7)
    try:
        admin_user = get_user_model().objects.get(id=7, username='admin')
        print(f"✓ Usuário encontrado: {admin_user.username}")
        print(f"  Email: {admin_user.email}")
        print(f"  Is_staff: {admin_user.is_staff}")
        print(f"  Is_superuser: {admin_user.is_superuser}")
        
        # Definir nova senha
        new_password = "admin123"
        admin_user.set_password(new_password)
        admin_user.save()
        
        print(f"\n✅ Senha redefinida com sucesso\!")
        print(f"\n📝 Credenciais de acesso:")
        print(f"   Username: admin")
        print(f"   Password: {new_password}")
        print(f"\n⚠️  IMPORTANTE: Altere esta senha após o primeiro login\!")
        
    except User.DoesNotExist:
        print("❌ Usuário admin (ID 7) não encontrado\!")
        
        # Listar admins disponíveis
        admins = get_user_model().objects.filter(is_superuser=True)
        if admins.exists():
            print("\n📋 Usuários admin disponíveis:")
            for admin in admins:
                print(f"   - ID: {admin.id}, Username: {admin.username}")
            
            # Tentar resetar o primeiro admin encontrado
            admin_user = admins.first()
            new_password = "admin123"
            admin_user.set_password(new_password)
            admin_user.save()
            
            print(f"\n✅ Senha redefinida para: {admin_user.username}")
            print(f"   Nova senha: {new_password}")
        else:
            print("\n❌ Nenhum usuário admin encontrado no sistema\!")
            print("💡 Você pode criar um novo admin com: python manage.py createsuperuser")

if __name__ == "__main__":
    reset_admin_password()
EOF < /dev/null
