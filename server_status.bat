@echo off
REM Script para verificar status do servidor Django

echo ========================================
echo   STATUS DO SERVIDOR DJANGO
echo ========================================
echo.

REM Verifica processos na porta 8080
echo [1] Verificando porta 8080...
netstat -an | findstr :8080 | findstr LISTENING >nul
if errorlevel 1 (
    echo    Status: PARADO
    echo    Nenhum processo escutando na porta 8080
) else (
    echo    Status: RODANDO
    echo.
    echo [2] Processos ativos:
    echo.
    
    REM Mostra detalhes dos processos
    for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8080 ^| findstr LISTENING') do (
        echo    PID: %%a
        
        REM Tenta obter nome do processo
        for /f "tokens=1" %%b in ('tasklist /FI "PID eq %%a" ^| findstr %%a') do (
            echo    Processo: %%b
        )
    )
)

echo.

REM Verifica arquivo PID
if exist server.pid (
    set /p SAVED_PID=<server.pid
    echo [3] PID salvo: %SAVED_PID%
) else (
    echo [3] Arquivo server.pid não encontrado
)

echo.

REM Testa conexão
echo [4] Testando conexão...
curl -s -o nul -w "   HTTP Status: %%{http_code}\n" http://localhost:8080 2>nul
if errorlevel 1 (
    echo    Falha ao conectar no servidor
)

echo.
echo ========================================
echo.
pause