@echo off
chcp 65001 > nul
title Instalador - Sistema Pizzaria

echo ========================================
echo   INSTALADOR DO SISTEMA PIZZARIA
echo ========================================
echo.

:: Verificar se Python está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERRO] Python não encontrado!
    echo Por favor, instale o Python 3.10 ou superior
    echo Download: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [OK] Python encontrado
echo.

:: Criar ambiente virtual se não existir
if not exist ".venv" (
    echo Criando ambiente virtual...
    python -m venv .venv
    echo [OK] Ambiente virtual criado
) else (
    echo [OK] Ambiente virtual já existe
)

:: Ativar ambiente virtual
echo Ativando ambiente virtual...
call .venv\Scripts\activate.bat

:: Instalar dependências
echo.
echo Instalando dependências...
pip install --upgrade pip
pip install -r requirements.txt
echo [OK] Dependências instaladas

:: Criar diretórios necessários
echo.
echo Criando diretórios...
if not exist "media" mkdir media
if not exist "staticfiles" mkdir staticfiles
if not exist "logs" mkdir logs
echo [OK] Diretórios criados

:: Executar migrações
echo.
echo Aplicando migrações do banco de dados...
python manage.py migrate --settings=settings_fast
echo [OK] Migrações aplicadas

:: Coletar arquivos estáticos
echo.
echo Coletando arquivos estáticos...
python manage.py collectstatic --noinput --settings=settings_fast
echo [OK] Arquivos estáticos coletados

:: Criar usuário admin se não existir
echo.
echo Deseja criar um usuário administrador? (S/N)
set /p criar_admin=
if /i "%criar_admin%"=="S" (
    python manage.py createsuperuser --settings=settings_fast
)

echo.
echo ========================================
echo   INSTALAÇÃO CONCLUÍDA COM SUCESSO!
echo ========================================
echo.
echo Para iniciar o servidor, use:
echo   iniciar_pizzaria.bat
echo.
echo Para acessar o sistema:
echo   http://localhost:8000
echo.
pause