"""
Comando para criar o usuário do sistema
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Cria o usuário do sistema usado pelo NoAuthMiddleware'
    
    def handle(self, *args, **options):
        username = 'sistema'
        
        try:
            user = User.objects.get(username=username)
            self.stdout.write(self.style.WARNING(f'Usuário "{username}" já existe'))
        except User.DoesNotExist:
            user = User.objects.create_user(
                username=username,
                email='sistema@pizzaria.com',
                password='senha_segura_2024',  # Senha forte mas não será usada
                first_name='Sistema',
                last_name='Pizzaria',
                is_staff=True,
                is_active=True
            )
            self.stdout.write(self.style.SUCCESS(f'✓ Usuário "{username}" criado com sucesso!'))
        
        # Mostra informações do usuário
        self.stdout.write(f"\nInformações do usuário:")
        self.stdout.write(f"ID: {user.id}")
        self.stdout.write(f"Username: {user.username}")
        self.stdout.write(f"Email: {user.email}")
        self.stdout.write(f"Nome: {user.get_full_name()}")
        self.stdout.write(f"Staff: {user.is_staff}")
        self.stdout.write(f"Ativo: {user.is_active}")