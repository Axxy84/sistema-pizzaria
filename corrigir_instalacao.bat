@echo off
chcp 65001 > nul
title Corrigir Instalação - Sistema Pizzaria

echo ╔════════════════════════════════════════════╗
echo ║     CORREÇÃO DE INSTALAÇÃO - PIZZARIA      ║
echo ╚════════════════════════════════════════════╝
echo.

:: 1. Corrigir problema do diretório static
echo [1/4] Criando diretório static no local correto...
cd /d "%~dp0"
if not exist "static" mkdir static
if not exist "static\css" mkdir static\css
if not exist "static\js" mkdir static\js
if not exist "static\images" mkdir static\images
echo [✓] Diretórios criados

:: 2. Deletar migração duplicada se existir
echo.
echo [2/4] Removendo migrações conflitantes...
if exist "apps\pedidos\migrations\0011_merge_20250722_1920.py" (
    del "apps\pedidos\migrations\0011_merge_20250722_1920.py"
    echo [✓] Migração duplicada removida
    
    :: Remover também o arquivo .pyc se existir
    if exist "apps\pedidos\migrations\__pycache__\0011_merge_20250722_1920.cpython*.pyc" (
        del "apps\pedidos\migrations\__pycache__\0011_merge_20250722_1920.cpython*.pyc"
    )
)

:: 3. Limpar cache do Python
echo.
echo [3/4] Limpando cache do Python...
if exist "apps\pedidos\migrations\__pycache__" (
    rmdir /s /q "apps\pedidos\migrations\__pycache__"
    mkdir "apps\pedidos\migrations\__pycache__"
)
echo [✓] Cache limpo

:: 4. Aplicar migrações
echo.
echo [4/4] Aplicando migrações corrigidas...
call .venv\Scripts\activate.bat
python manage.py migrate --settings=settings_fast
if %errorlevel% equ 0 (
    echo [✓] Migrações aplicadas com sucesso!
) else (
    echo [!] Ainda há problemas. Tentando resolver...
    python manage.py migrate --fake pedidos 0010 --settings=settings_fast
    python manage.py migrate --settings=settings_fast
)

echo.
echo ╔════════════════════════════════════════════╗
echo ║          CORREÇÕES APLICADAS!              ║
echo ╠════════════════════════════════════════════╣
echo ║  Agora execute: instalar_windows_v2.bat    ║
echo ╚════════════════════════════════════════════╝
echo.
pause