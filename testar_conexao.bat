@echo off
chcp 65001 > nul
title Testar Conexão Supabase - Sistema Pizzaria

echo ╔════════════════════════════════════════════╗
echo ║     TESTANDO CONEXÃO COM SUPABASE          ║
echo ╚════════════════════════════════════════════╝
echo.

cd /d "%~dp0"

:: Verificar se ambiente virtual existe
if not exist ".venv" (
    echo [!] Ambiente virtual não encontrado!
    echo Execute primeiro: python -m venv .venv
    pause
    exit /b 1
)

:: Ativar ambiente virtual
call .venv\Scripts\activate.bat

:: Verificar se .env existe
if not exist ".env" (
    echo [!] Arquivo .env não encontrado!
    echo.
    echo Criando arquivo .env de exemplo...
    (
        echo # Configurações do Supabase
        echo DATABASE_HOST=aws-0-sa-east-1.pooler.supabase.com
        echo DATABASE_PORT=5432
        echo DATABASE_NAME=postgres
        echo DATABASE_USER=postgres.aewcurtmikqelqykpqoa
        echo DATABASE_PASSWORD=COLOQUE_SUA_SENHA_AQUI
        echo.
        echo # Outras configurações
        echo DEBUG=True
        echo SECRET_KEY=django-insecure-development-key
    ) > .env
    
    echo.
    echo ╔════════════════════════════════════════════╗
    echo ║              AÇÃO NECESSÁRIA!              ║
    echo ╠════════════════════════════════════════════╣
    echo ║                                            ║
    echo ║  1. Abra o arquivo .env                    ║
    echo ║  2. Substitua COLOQUE_SUA_SENHA_AQUI       ║
    echo ║     pela sua senha do Supabase             ║
    echo ║  3. Execute este script novamente          ║
    echo ║                                            ║
    echo ╚════════════════════════════════════════════╝
    echo.
    pause
    exit /b 1
)

:: Instalar python-dotenv se necessário
pip show python-dotenv >nul 2>&1
if %errorlevel% neq 0 (
    echo Instalando python-dotenv...
    pip install python-dotenv
)

:: Executar teste
echo.
python testar_supabase.py

echo.
echo ╔════════════════════════════════════════════╗
echo ║         DIAGNÓSTICO CONCLUÍDO              ║
echo ╠════════════════════════════════════════════╣
echo ║                                            ║
echo ║  Se houver erros acima:                   ║
echo ║  1. Verifique sua senha no .env           ║
echo ║  2. Confirme as credenciais do Supabase   ║
echo ║  3. Execute: python manage.py migrate      ║
echo ║                                            ║
echo ╚════════════════════════════════════════════╝
echo.
pause