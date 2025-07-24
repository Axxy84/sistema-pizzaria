@echo off
echo ============================================
echo   REINICIAR SERVIDOR DJANGO
echo ============================================
echo.

echo [1] Parando servidor atual...
echo.

REM Para o serviço Windows
net stop DjangoPizzariaAuto 2>nul
net stop DjangoPizzaria 2>nul

REM Mata processos Python
taskkill /F /IM python.exe >nul 2>&1

REM Limpa portas
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8080') do (
    taskkill /F /PID %%a >nul 2>&1
)

echo.
echo [2] Aguardando 3 segundos...
timeout /t 3 /nobreak >nul

echo.
echo [3] Iniciando servidor...
echo.

REM Verifica qual método usar
if exist "nssm.exe" (
    echo Iniciando via servico Windows...
    net start DjangoPizzariaAuto
) else (
    echo Iniciando via script VBS em background...
    start "" /B wscript servidor_background_vbs.vbs
)

echo.
echo [4] Verificando se iniciou...
timeout /t 5 /nobreak >nul

netstat -an | findstr :8080 | findstr LISTENING
if errorlevel 1 (
    echo.
    echo [!] Servidor nao iniciou automaticamente
    echo     Iniciando manualmente...
    echo.
    call .venv\Scripts\activate.bat
    python manage.py runserver 0.0.0.0:8080
) else (
    echo.
    echo [OK] Servidor rodando em background!
    echo     Acesse: http://localhost:8080
)

pause