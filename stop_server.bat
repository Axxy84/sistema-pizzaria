@echo off
REM Script para parar o servidor Django rodando em segundo plano

echo ========================================
echo   PARANDO SERVIDOR DJANGO
echo ========================================
echo.

REM Verifica se existe arquivo com PID
if exist server.pid (
    set /p PID=<server.pid
    echo [1] Parando processo com PID: %PID%
    taskkill /F /PID %PID% >nul 2>&1
    del server.pid
) else (
    echo [1] Arquivo server.pid não encontrado
)

REM Para garantir, mata todos os processos Python na porta 8080
echo [2] Verificando outros processos na porta 8080...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8080 ^| findstr LISTENING') do (
    echo    Finalizando processo PID: %%a
    taskkill /F /PID %%a >nul 2>&1
)

REM Verifica se ainda há processos
netstat -an | findstr :8080 | findstr LISTENING >nul
if errorlevel 1 (
    echo.
    echo [SUCESSO] Servidor parado com sucesso!
) else (
    echo.
    echo [AVISO] Ainda existem processos na porta 8080
    echo Tente executar este script como Administrador
)

echo.
pause