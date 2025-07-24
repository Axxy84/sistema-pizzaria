#!/usr/bin/env python
"""
Servidor Django simples e direto
"""
import os
import sys

# Adicionar o diretório atual ao Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoProject.settings')

# Importar e configurar Django
import django
django.setup()

# Executar o servidor
from django.core.management import execute_from_command_line

print("\n" + "="*60)
print("  SERVIDOR DJANGO - MODO SIMPLES")
print("="*60)
print("\nIniciando em: http://localhost:8080")
print("              http://127.0.0.1:8080")
print("\nPressione CTRL+C para parar")
print("-"*60 + "\n")

# Executar comando runserver
execute_from_command_line(['manage.py', 'runserver', '127.0.0.1:8080'])