#!/usr/bin/env python
"""
Script para testar e diagnosticar conexão com Supabase
"""
import os
import sys
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

print("=" * 60)
print("TESTE DE CONEXÃO COM SUPABASE")
print("=" * 60)
print()

# 1. Verificar variáveis de ambiente
print("1. VARIÁVEIS DE AMBIENTE:")
print("-" * 40)
db_vars = {
    'DATABASE_HOST': os.getenv('DATABASE_HOST', 'aws-0-sa-east-1.pooler.supabase.com'),
    'DATABASE_PORT': os.getenv('DATABASE_PORT', '5432'),
    'DATABASE_NAME': os.getenv('DATABASE_NAME', 'postgres'),
    'DATABASE_USER': os.getenv('DATABASE_USER', 'postgres.aewcurtmikqelqykpqoa'),
    'DATABASE_PASSWORD': os.getenv('DATABASE_PASSWORD', 'NÃO DEFINIDA')
}

for key, value in db_vars.items():
    if key == 'DATABASE_PASSWORD':
        if value == 'NÃO DEFINIDA':
            print(f"❌ {key}: {value}")
        else:
            print(f"✅ {key}: {'*' * len(value)}")
    else:
        print(f"✅ {key}: {value}")

print()

# 2. Testar conexão com psycopg2
print("2. TESTE DE CONEXÃO DIRETA (psycopg2):")
print("-" * 40)
try:
    import psycopg2
    
    if db_vars['DATABASE_PASSWORD'] == 'NÃO DEFINIDA':
        print("❌ ERRO: Senha do banco não está definida no .env!")
        print("   Configure DATABASE_PASSWORD no arquivo .env")
        sys.exit(1)
    
    conn = psycopg2.connect(
        host=db_vars['DATABASE_HOST'],
        database=db_vars['DATABASE_NAME'],
        user=db_vars['DATABASE_USER'],
        password=db_vars['DATABASE_PASSWORD'],
        port=db_vars['DATABASE_PORT'],
        sslmode='require'
    )
    
    print("✅ Conexão estabelecida com sucesso!")
    
    # Testar query simples
    cursor = conn.cursor()
    cursor.execute("SELECT version();")
    version = cursor.fetchone()
    print(f"✅ PostgreSQL versão: {version[0].split(',')[0]}")
    
    cursor.close()
    conn.close()
    
except ImportError:
    print("❌ ERRO: psycopg2 não está instalado!")
    print("   Execute: pip install psycopg2-binary")
except psycopg2.OperationalError as e:
    print(f"❌ ERRO de conexão: {str(e)}")
    print("\nPossíveis causas:")
    print("1. Senha incorreta")
    print("2. Usuário incorreto") 
    print("3. Host/porta incorretos")
    print("4. Firewall bloqueando conexão")
except Exception as e:
    print(f"❌ ERRO inesperado: {str(e)}")

print()

# 3. Testar conexão Django
print("3. TESTE DE CONEXÃO DJANGO:")
print("-" * 40)
try:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoProject.settings')
    import django
    django.setup()
    
    from django.db import connection
    
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        print("✅ Conexão Django funcionando!")
        
    # Verificar tabelas
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            ORDER BY table_name;
        """)
        tables = cursor.fetchall()
        print(f"✅ {len(tables)} tabelas encontradas no banco")
        
        # Verificar se tabela pedidos existe
        table_names = [t[0] for t in tables]
        if 'pedidos_pedido' in table_names:
            print("✅ Tabela 'pedidos_pedido' existe")
            
            # Verificar colunas
            cursor.execute("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'pedidos_pedido'
                ORDER BY ordinal_position;
            """)
            columns = cursor.fetchall()
            column_names = [c[0] for c in columns]
            
            if 'status' in column_names:
                print("✅ Coluna 'status' existe na tabela")
            else:
                print("❌ Coluna 'status' NÃO existe na tabela!")
                print("   Execute: python manage.py migrate")
        else:
            print("❌ Tabela 'pedidos_pedido' NÃO existe!")
            print("   Execute: python manage.py migrate")
            
except Exception as e:
    print(f"❌ ERRO Django: {str(e)}")

print()

# 4. Verificar migrações
print("4. STATUS DAS MIGRAÇÕES:")
print("-" * 40)
try:
    from django.core.management import call_command
    from io import StringIO
    
    out = StringIO()
    call_command('showmigrations', '--plan', stdout=out)
    migrations = out.getvalue()
    
    # Contar migrações aplicadas e pendentes
    lines = migrations.split('\n')
    applied = sum(1 for line in lines if '[X]' in line)
    pending = sum(1 for line in lines if '[ ]' in line)
    
    print(f"✅ Migrações aplicadas: {applied}")
    if pending > 0:
        print(f"❌ Migrações pendentes: {pending}")
        print("   Execute: python manage.py migrate")
    else:
        print("✅ Todas as migrações foram aplicadas")
        
except Exception as e:
    print(f"❌ Erro ao verificar migrações: {str(e)}")

print()
print("=" * 60)
print("FIM DO DIAGNÓSTICO")
print("=" * 60)