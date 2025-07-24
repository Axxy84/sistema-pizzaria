@echo off
echo ============================================
echo   LOGS DO SERVICO WINDOWS
echo ============================================
echo.

echo [1] Verificando se o servico esta rodando...
sc query DjangoPizzaria | findstr STATE
echo.

echo [2] Verificando porta 8080...
netstat -an | findstr :8080
echo.

echo [3] Logs do servico:
echo ============================================
echo.

if exist "logs\service\servico.log" (
    echo === SERVICO.LOG (ultimas 50 linhas) ===
    powershell -Command "Get-Content 'logs\service\servico.log' -Tail 50"
    echo.
) else (
    echo [!] Arquivo servico.log nao encontrado
)

if exist "logs\service\erro.log" (
    echo.
    echo === ERRO.LOG (ultimas 50 linhas) ===
    powershell -Command "Get-Content 'logs\service\erro.log' -Tail 50"
) else (
    echo [!] Arquivo erro.log nao encontrado
)

if exist "logs\service\wrapper.log" (
    echo.
    echo === WRAPPER.LOG ===
    type "logs\service\wrapper.log"
) else (
    echo [!] Arquivo wrapper.log nao encontrado
)

echo.
echo ============================================
echo.
pause