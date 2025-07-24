@echo off
echo ============================================
echo   PARAR SERVIDOR DJANGO
echo ============================================
echo.

echo [1] Parando servico Windows...
net stop DjangoPizzariaAuto 2>nul
net stop DjangoPizzaria 2>nul

echo.
echo [2] Finalizando processos Python...
taskkill /F /IM python.exe

echo.
echo [3] Liberando porta 8080...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8080') do (
    echo Matando processo PID: %%a
    taskkill /F /PID %%a
)

echo.
echo [4] Verificando...
netstat -an | findstr :8080
if errorlevel 1 (
    echo.
    echo [OK] Servidor parado com sucesso!
) else (
    echo.
    echo [!] Ainda ha processos na porta 8080
)

echo.
pause