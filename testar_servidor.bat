@echo off
echo ============================================
echo   TESTE COMPLETO DO SERVIDOR
echo ============================================
echo.

echo [1] Parando servico...
net stop DjangoPizzaria >nul 2>&1

echo [2] Limpando porta 8080...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8080') do (
    taskkill /F /PID %%a >nul 2>&1
)

echo [3] Testando servidor diretamente...
echo.
echo Se funcionar aqui, o problema e no servico Windows.
echo.
echo Iniciando servidor (Ctrl+C para parar)...
echo ============================================
echo.

call .venv\Scripts\activate.bat
python manage.py runserver 0.0.0.0:8080