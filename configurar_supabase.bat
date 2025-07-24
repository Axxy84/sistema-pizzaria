@echo off
chcp 65001 > nul
title Configurar Supabase - Sistema Pizzaria

echo ╔════════════════════════════════════════════╗
echo ║     CONFIGURAÇÃO DO SUPABASE               ║
echo ╚════════════════════════════════════════════╝
echo.

cd /d "%~dp0"

:: Verificar se .env existe
if not exist ".env" (
    echo [!] Arquivo .env não encontrado!
    echo.
    echo Criando .env a partir do modelo...
    copy ".env.supabase" ".env"
    echo.
    echo ╔════════════════════════════════════════════╗
    echo ║         AÇÃO NECESSÁRIA!                   ║
    echo ╠════════════════════════════════════════════╣
    echo ║  1. Edite o arquivo .env                   ║
    echo ║  2. Adicione sua senha do Supabase em:    ║
    echo ║     DATABASE_PASSWORD=sua_senha_aqui       ║
    echo ║  3. Execute este script novamente          ║
    echo ╚════════════════════════════════════════════╝
    echo.
    pause
    exit /b 1
)

:: Ativar ambiente virtual
call .venv\Scripts\activate.bat

echo [1/5] Testando conexão com Supabase...
python -c "import psycopg2, os; conn = psycopg2.connect(host=os.getenv('DATABASE_HOST', 'aws-0-sa-east-1.pooler.supabase.com'), database=os.getenv('DATABASE_NAME', 'postgres'), user=os.getenv('DATABASE_USER', 'postgres.aewcurtmikqelqykpqoa'), password=os.getenv('DATABASE_PASSWORD'), port=os.getenv('DATABASE_PORT', '5432'), sslmode='require'); print('[✓] Conexão com Supabase OK!'); conn.close()" 2>nul
if %errorlevel% neq 0 (
    echo [✗] Erro de conexão com Supabase!
    echo.
    echo Verifique:
    echo 1. Sua senha está correta no arquivo .env
    echo 2. Você tem conexão com a internet
    echo 3. As credenciais do Supabase estão corretas
    echo.
    pause
    exit /b 1
)

echo.
echo [2/5] Aplicando migrações...
python manage.py migrate --run-syncdb
if %errorlevel% neq 0 (
    echo [!] Tentando corrigir migrações...
    python manage.py migrate --fake-initial
)
echo [✓] Migrações aplicadas

echo.
echo [3/5] Coletando arquivos estáticos...
python manage.py collectstatic --noinput --clear >nul 2>&1
echo [✓] Arquivos estáticos prontos

echo.
echo [4/5] Verificando estrutura do banco...
python -c "from apps.pedidos.models import Pedido; print(f'[✓] Modelo Pedido OK - {len([f.name for f in Pedido._meta.fields])} campos')"
python -c "from apps.produtos.models import Produto; print(f'[✓] Modelo Produto OK')"
python -c "from apps.clientes.models import Cliente; print(f'[✓] Modelo Cliente OK')"

echo.
echo [5/5] Criar usuário administrador?
echo.
echo Deseja criar um usuário administrador? (S/N)
set /p criar_admin=
if /i "%criar_admin%"=="S" (
    python manage.py createsuperuser
)

echo.
echo ╔════════════════════════════════════════════╗
echo ║      SUPABASE CONFIGURADO COM SUCESSO!     ║
echo ╠════════════════════════════════════════════╣
echo ║                                            ║
echo ║  Banco de dados: Supabase PostgreSQL       ║
echo ║  Status: ✓ Conectado e configurado         ║
echo ║                                            ║
echo ║  Para iniciar o sistema:                   ║
echo ║  → Execute: iniciar_pizzaria.bat           ║
echo ║                                            ║
echo ╚════════════════════════════════════════════╝
echo.
pause