"""
Script para criar o usuário do sistema no banco
Execute este script no ambiente Windows onde o banco está acessível
"""
import os
import sys
import django

# Configura o Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoProject.settings')
django.setup()

from django.contrib.auth.models import User

def criar_usuario_sistema():
    """Cria o usuário do sistema"""
    username = 'sistema'
    
    try:
        # Verifica se já existe
        user = User.objects.get(username=username)
        print(f"✓ Usuário '{username}' já existe!")
        print(f"  ID: {user.id}")
        print(f"  Email: {user.email}")
        print(f"  Nome: {user.get_full_name()}")
        
    except User.DoesNotExist:
        # Cria o usuário
        user = User.objects.create_user(
            username=username,
            email='sistema@pizzaria.com',
            password='senha_sistema_2024',  # Senha forte mas não será usada
            first_name='Sistema',
            last_name='Pizzaria',
            is_staff=True,
            is_active=True
        )
        print(f"✓ Usuário '{username}' criado com sucesso!")
        print(f"  ID: {user.id}")
        print(f"  Email: {user.email}")
        print(f"  Nome: {user.get_full_name()}")
        
    return user

if __name__ == '__main__':
    print("=== Criando usuário do sistema ===")
    try:
        criar_usuario_sistema()
        print("\n✓ Processo concluído com sucesso!")
    except Exception as e:
        print(f"\n✗ Erro: {e}")
        print("\nVerifique se:")
        print("1. O banco de dados está acessível")
        print("2. As configurações do banco estão corretas no .env")
        print("3. Você está executando no ambiente correto")