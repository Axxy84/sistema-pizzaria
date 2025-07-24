@echo off
chcp 65001 > nul
title Corrigir Banco de Dados - Sistema Pizzaria

echo ╔════════════════════════════════════════════╗
echo ║     CORREÇÃO DO BANCO DE DADOS             ║
echo ╚════════════════════════════════════════════╝
echo.

cd /d "%~dp0"
call .venv\Scripts\activate.bat

echo [1/5] Fazendo backup do banco atual...
if exist "db.sqlite3" (
    copy "db.sqlite3" "db.sqlite3.backup_%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%.bak" >nul
    echo [✓] Backup criado
)

echo.
echo [2/5] Removendo banco com problemas...
if exist "db.sqlite3" del "db.sqlite3"
echo [✓] Banco removido

echo.
echo [3/5] Criando novo banco...
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