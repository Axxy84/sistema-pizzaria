from django.core.management.base import BaseCommand
from django.conf import settings
import getpass
import os


class Command(BaseCommand):
    help = 'Define ou altera a senha para cancelamento de pedidos'

    def add_arguments(self, parser):
        parser.add_argument(
            '--password',
            type=str,
            help='Nova senha (se não fornecida, será solicitada interativamente)',
        )
        parser.add_argument(
            '--show',
            action='store_true',
            help='Mostra a senha atual',
        )

    def handle(self, *args, **options):
        # Mostrar senha atual
        if options['show']:
            current_password = getattr(settings, 'ADMIN_CANCEL_PASSWORD', None)
            if current_password:
                self.stdout.write(
                    self.style.WARNING(f'Senha atual: {current_password}')
                )
                self.stdout.write(
                    self.style.WARNING('ATENÇÃO: Esta senha deve ser mantida em segredo!')
                )
            else:
                self.stdout.write(
                    self.style.ERROR('Nenhuma senha configurada.')
                )
            return

        # Obter nova senha
        if options['password']:
            new_password = options['password']
        else:
            # Solicitar senha interativamente
            while True:
                new_password = getpass.getpass('Digite a nova senha para cancelamento: ')
                if not new_password:
                    self.stdout.write(
                        self.style.ERROR('A senha não pode estar vazia!')
                    )
                    continue
                
                confirm_password = getpass.getpass('Confirme a nova senha: ')
                
                if new_password != confirm_password:
                    self.stdout.write(
                        self.style.ERROR('As senhas não coincidem! Tente novamente.')
                    )
                    continue
                
                break

        # Caminho do arquivo settings.py
        settings_path = os.path.join(settings.BASE_DIR, 'DjangoProject', 'settings.py')
        
        try:
            # Ler o arquivo settings.py
            with open(settings_path, 'r') as file:
                lines = file.readlines()
            
            # Procurar e atualizar a linha da senha
            updated = False
            for i, line in enumerate(lines):
                if line.strip().startswith('ADMIN_CANCEL_PASSWORD'):
                    lines[i] = f"ADMIN_CANCEL_PASSWORD = '{new_password}'  # Senha padrão - MUDE ISSO!\n"
                    updated = True
                    break
            
            # Se não encontrou, adicionar no final do arquivo
            if not updated:
                # Procurar onde inserir (antes de REST_FRAMEWORK)
                for i, line in enumerate(lines):
                    if 'REST_FRAMEWORK' in line:
                        lines.insert(i, f"\n# Senha para cancelamento de pedidos\n")
                        lines.insert(i+1, f"# IMPORTANTE: Altere esta senha em produção!\n")
                        lines.insert(i+2, f"ADMIN_CANCEL_PASSWORD = '{new_password}'  # Senha padrão - MUDE ISSO!\n")
                        lines.insert(i+3, "\n")
                        updated = True
                        break
            
            # Escrever de volta no arquivo
            with open(settings_path, 'w') as file:
                file.writelines(lines)
            
            self.stdout.write(
                self.style.SUCCESS(f'✅ Senha alterada com sucesso!')
            )
            self.stdout.write(
                self.style.WARNING(f'Nova senha: {new_password}')
            )
            self.stdout.write(
                self.style.WARNING('IMPORTANTE: Reinicie o servidor Django para aplicar a mudança!')
            )
            self.stdout.write(
                self.style.NOTICE('Execute: python manage.py runserver')
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Erro ao atualizar settings.py: {str(e)}')
            )
            self.stdout.write(
                self.style.ERROR('Você pode atualizar manualmente no arquivo settings.py')
            )
            self.stdout.write(
                self.style.WARNING(f"ADMIN_CANCEL_PASSWORD = '{new_password}'")
            )