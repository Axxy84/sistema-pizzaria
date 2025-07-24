@echo off
echo ============================================
echo   TESTE COM SERVIDOR SIMPLES
echo ============================================
echo.

echo [1] Parando processos anteriores...
taskkill /F /IM python.exe >nul 2>&1
timeout /t 2 /nobreak >nul

echo.
echo [2] Ativando ambiente virtual...
call .venv\Scripts\activate.bat

echo.
echo [3] Iniciando servidor simples...
echo.
python servidor_simples.py