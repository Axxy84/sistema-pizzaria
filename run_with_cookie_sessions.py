#!/usr/bin/env python
"""
Script para rodar o servidor Django com sessões em cookies
(solução temporária enquanto a senha do PostgreSQL não é corrigida)
"""

import os
import sys
import subprocess

# Definir as configurações temporárias
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings_temp_session'

print("=" * 60)
print("🚀 INICIANDO SERVIDOR COM SESSÕES EM COOKIES")
print("=" * 60)
print()
print("⚠️  ATENÇÃO: Esta é uma solução TEMPORÁRIA!")
print()
print("Para corrigir permanentemente:")
print("1. Abra o arquivo .env")
print("2. Atualize DATABASE_PASSWORD com a senha correta do Supabase")
print("3. Use 'python manage.py runserver' normalmente")
print()
print("=" * 60)
print()

# Executar o servidor
subprocess.run([sys.executable, 'manage.py', 'runserver'])