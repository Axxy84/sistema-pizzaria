#!/usr/bin/env python
"""
Script para resetar senha do admin para facilitar acesso
"""
import os
import sys
import django

# Setup Django
sys.path.append('/home/labdev/Documentos/DjangoProject')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoProject.settings')
django.setup()

from django.contrib.auth.models import User

def reset_admin_password():
    """Resetar senha do admin para 'admin123'"""
    try:
        admin = User.objects.get(username='admin')
        admin.set_password('admin123')
        admin.save()
        print("✅ Senha do admin resetada com sucesso!")
        print("📧 Email: admin@example.com")
        print("🔑 Senha: admin123")
        return True
    except User.DoesNotExist:
        print("❌ Usuário admin não encontrado")
        return False

def create_admin_if_not_exists():
    """Criar admin se não existir"""
    if not User.objects.filter(username='admin').exists():
        admin = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )
        print("✅ Usuário admin criado com sucesso!")
        print("📧 Email: admin@example.com")
        print("🔑 Senha: admin123")
        return True
    return False

def main():
    print("🔧 Configurando acesso de admin...")
    
    if create_admin_if_not_exists():
        print("\n✅ Admin criado!")
    else:
        if reset_admin_password():
            print("\n✅ Senha resetada!")
    
    print("\n🌐 Agora você pode acessar:")
    print("1. http://127.0.0.1:8001/auth/login/")
    print("2. Use: admin@example.com / admin123")
    print("3. Depois acesse: http://127.0.0.1:8001/estoque/")

if __name__ == '__main__':
    main()