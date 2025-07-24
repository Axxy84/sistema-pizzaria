@echo off
chcp 65001 > nul
title Sistema Pizzaria - Servidor

:: Definir diretório do projeto
set PROJECT_DIR=%~dp0
cd /d "%PROJECT_DIR%"

:: Ativar ambiente virtual
if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
) else (
    echo [ERRO] Ambiente virtual não encontrado!
    echo Execute instalar_windows.bat primeiro
    pause
    exit /b 1
)

:: Configurar variáveis de ambiente
set DJANGO_SETTINGS_MODULE=settings_fast
set PYTHONDONTWRITEBYTECODE=1

:: Limpar tela
cls

echo ========================================
echo   SISTEMA PIZZARIA - INICIANDO
echo ========================================
echo.
echo Servidor iniciando em http://localhost:8000
echo.
echo Pressione Ctrl+C para parar o servidor
echo ========================================
echo.

:: Iniciar servidor
python manage.py runserver 0.0.0.0:8000 --settings=settings_fast

pause