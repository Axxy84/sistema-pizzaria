@echo off
chcp 65001 > nul
title Remover SQLite - Sistema Pizzaria

echo ╔════════════════════════════════════════════╗
echo ║     REMOVENDO TODOS OS ARQUIVOS SQLITE     ║
echo ╚════════════════════════════════════════════╝
echo.

cd /d "%~dp0"

echo Procurando arquivos SQLite...
echo.

:: Remover arquivos SQLite
if exist "db.sqlite3" (
    del "db.sqlite3"
    echo [✓] db.sqlite3 removido
)

if exist "*.sqlite3" (
    del "*.sqlite3"
    echo [✓] Arquivos .sqlite3 removidos
)

if exist "*.db" (
    del "*.db"
    echo [✓] Arquivos .db removidos
)

:: Remover backups SQLite
if exist "*.sqlite3.backup*" (
    del "*.sqlite3.backup*"
    echo [✓] Backups SQLite removidos
)

if exist "*.bak" (
    del "*.bak"
    echo [✓] Arquivos .bak removidos
)

echo.
echo ╔════════════════════════════════════════════╗
echo ║        LIMPEZA CONCLUÍDA!                  ║
echo ╠════════════════════════════════════════════╣
echo ║  O sistema agora usa APENAS Supabase       ║
echo ║                                            ║
echo ║  Configure seu .env com as credenciais:    ║
echo ║  1. Copie .env.supabase para .env          ║
echo ║  2. Adicione sua senha do Supabase         ║
echo ╚════════════════════════════════════════════╝
echo.
pause