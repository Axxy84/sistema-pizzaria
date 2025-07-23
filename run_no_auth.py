#!/usr/bin/env python
"""
Script para executar o sistema SEM AUTENTICAÇÃO
APENAS PARA DESENVOLVIMENTO LOCAL!
"""

import os
import sys
import subprocess

# Configurar para usar as settings sem autenticação
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings_no_auth'

# Banner de aviso
print("\n" + "🚨"*30)
print("\n⚠️  INICIANDO SISTEMA SEM AUTENTICAÇÃO!")
print("⚠️  ISSO É EXTREMAMENTE INSEGURO!")
print("⚠️  USE APENAS PARA DESENVOLVIMENTO LOCAL!")
print("\n" + "🚨"*30 + "\n")

print("O sistema será iniciado com:")
print("✅ Acesso livre a todas as páginas")
print("✅ Usuário temporário com permissões totais")
print("✅ Sem necessidade de login")
print("✅ Sem verificação CSRF")
print("\nPara parar: CTRL+C")
print("\n" + "-"*60 + "\n")

# Perguntar confirmação
resposta = input("Tem certeza que deseja continuar? (digite 'SIM' para confirmar): ")

if resposta.upper() != 'SIM':
    print("\n❌ Operação cancelada.")
    sys.exit(0)

print("\n🚀 Iniciando servidor...\n")

# Executar o servidor
try:
    subprocess.run([sys.executable, 'manage.py', 'runserver'])
except KeyboardInterrupt:
    print("\n\n✋ Servidor parado.")
    print("Para usar o sistema normalmente, execute: python manage.py runserver")