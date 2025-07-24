@echo off
REM Script para visualizar os logs do servidor

echo ========================================
echo   LOGS DO SERVIDOR DJANGO
echo ========================================
echo.

REM Verifica se existe pasta de logs
if not exist "logs" (
    echo [ERRO] Pasta de logs não encontrada!
    echo Execute run_background.bat primeiro.
    pause
    exit /b 1
)

REM Lista arquivos de log disponíveis
echo Arquivos de log disponíveis:
echo.
dir /b /o-d logs\*.log 2>nul
if errorlevel 1 (
    echo Nenhum arquivo de log encontrado.
    pause
    exit /b 1
)

echo.
echo ========================================

REM Pega o arquivo de log mais recente
for /f "delims=" %%i in ('dir /b /o-d logs\*.log') do (
    set LATEST_LOG=logs\%%i
    goto :found
)

:found
echo Mostrando log mais recente: %LATEST_LOG%
echo ========================================
echo.

REM Mostra o conteúdo do log
type "%LATEST_LOG%"

echo.
echo ========================================
echo Pressione qualquer tecla para sair...
pause >nul