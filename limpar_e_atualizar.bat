@echo off
chcp 65001 > nul
title Limpeza e Atualização do Sistema

echo ========================================
echo   LIMPEZA E ATUALIZAÇÃO DO SISTEMA
echo ========================================
echo.
echo ATENÇÃO: Este script irá:
echo - Fazer backup de arquivos importantes
echo - Limpar arquivos conflitantes
echo - Atualizar o código do GitHub
echo.
echo Pressione Ctrl+C para cancelar ou
pause

:: Criar pasta de backup
echo.
echo Criando backup...
if not exist "backup" mkdir backup
copy *.bat backup\ >nul 2>&1
copy .env backup\ >nul 2>&1
echo [OK] Backup criado na pasta 'backup'

:: Remover arquivos problemáticos
echo.
echo Removendo arquivos conflitantes...
del /f "C:\Users\User\Documents\sistema-pizzaria-master\.env.correto" >nul 2>&1
del /f "C:\Users\User\Documents\sistema-pizzaria-master\atualizar.bat" >nul 2>&1
del /f "C:\Users\User\Documents\sistema-pizzaria-master\debug_env.py" >nul 2>&1
del /f "C:\Users\User\Documents\sistema-pizzaria-master\enviar_mudancas.bat" >nul 2>&1
del /f "C:\Users\User\Documents\sistema-pizzaria-master\receber_mudancas.bat" >nul 2>&1
del /f "C:\Users\User\Documents\sistema-pizzaria-master\test_supabase.py" >nul 2>&1
echo [OK] Arquivos conflitantes removidos

:: Resetar mudanças locais não commitadas
echo.
echo Resetando mudanças locais...
git reset --hard HEAD
echo [OK] Reset concluído

:: Atualizar do repositório
echo.
echo Atualizando código do GitHub...
git pull origin master

:: Verificar se deu certo
if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo   ✅ ATUALIZAÇÃO CONCLUÍDA!
    echo ========================================
    echo.
    echo Agora execute:
    echo   iniciar_pizzaria.bat
    echo.
) else (
    echo.
    echo ========================================
    echo   ❌ ERRO NA ATUALIZAÇÃO
    echo ========================================
    echo.
    echo Tente executar manualmente:
    echo   git reset --hard origin/master
    echo.
)

pause