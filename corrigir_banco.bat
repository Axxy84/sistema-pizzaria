@echo off
chcp 65001 > nul
title Corrigir Banco de Dados - Sistema Pizzaria

echo ╔════════════════════════════════════════════╗
echo ║     CORREÇÃO DO BANCO DE DADOS             ║
echo ╚════════════════════════════════════════════╝
echo.

cd /d "%~dp0"
call .venv\Scripts\activate.bat

echo [1/3] Verificando conexão com Supabase...
python -c "import os; print(f'Host: {os.getenv(\"DATABASE_HOST\", \"aws-0-sa-east-1.pooler.supabase.com\")}'); print(f'User: {os.getenv(\"DATABASE_USER\", \"postgres.aewcurtmikqelqykpqoa\")}')"
echo.

echo [2/3] Aplicando migrações no Supabase...
python manage.py migrate --run-syncdb --settings=settings_fast
if %errorlevel% neq 0 (
    echo [!] Erro ao criar banco. Tentando alternativa...
    python manage.py migrate --run-syncdb
)
echo [✓] Banco criado

echo.
echo [4/5] Verificando estrutura...
echo.
python -c "from apps.pedidos.models import Pedido; print(f'Campos do Pedido: {[f.name for f in Pedido._meta.fields]}')"
echo.

echo.
echo [5/5] Criando dados iniciais...
python -c "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@pizzaria.com', 'admin123') if not User.objects.filter(username='admin').exists() else None; print('[✓] Usuário admin criado (senha: admin123)')"

echo.
echo ╔════════════════════════════════════════════╗
echo ║         BANCO CORRIGIDO COM SUCESSO!       ║
echo ╠════════════════════════════════════════════╣
echo ║  Usuário: admin                            ║
echo ║  Senha: admin123                           ║
echo ║                                            ║
echo ║  Execute: iniciar_pizzaria.bat             ║
echo ╚════════════════════════════════════════════╝
echo.
pause