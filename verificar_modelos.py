#!/usr/bin/env python
"""
Script para verificar e diagnosticar problemas nos modelos
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoProject.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from apps.pedidos.models import Pedido
from django.db import connection

def verificar_estrutura():
    print("=== VERIFICAÇÃO DA ESTRUTURA DO BANCO ===\n")
    
    # 1. Verificar campos do modelo
    print("1. Campos definidos no modelo Pedido:")
    for field in Pedido._meta.fields:
        print(f"   - {field.name} ({field.get_internal_type()})")
    
    # 2. Verificar estrutura real da tabela
    print("\n2. Estrutura real da tabela no banco:")
    with connection.cursor() as cursor:
        # Para SQLite
        cursor.execute("PRAGMA table_info(pedidos_pedido)")
        columns = cursor.fetchall()
        if columns:
            print("   Colunas encontradas:")
            for col in columns:
                print(f"   - {col[1]} ({col[2]})")
        else:
            print("   [!] Tabela não existe!")
    
    # 3. Verificar se campo status existe
    print("\n3. Verificação do campo 'status':")
    column_names = [col[1] for col in columns] if columns else []
    if 'status' in column_names:
        print("   [✓] Campo 'status' existe na tabela")
    else:
        print("   [✗] Campo 'status' NÃO existe na tabela")
        print("   [!] Isso explica o erro!")
    
    # 4. Verificar migrações pendentes
    print("\n4. Migrações pendentes:")
    from django.core.management import call_command
    from io import StringIO
    out = StringIO()
    call_command('showmigrations', 'pedidos', stdout=out)
    migrations = out.getvalue()
    print(migrations)
    
    # 5. Sugestões
    print("\n=== SUGESTÕES DE CORREÇÃO ===")
    if 'status' not in column_names:
        print("1. Execute: python manage.py migrate --fake-initial")
        print("2. Ou delete o banco e execute: python manage.py migrate")
        print("3. Ou use o script: corrigir_banco.bat")

if __name__ == "__main__":
    verificar_estrutura()