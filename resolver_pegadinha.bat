@echo off
echo ============================================
echo   RESOLVENDO A PEGADINHA SERVIDOR/FRONTEND
echo ============================================
echo.

echo [1] Parando tudo...
net stop DjangoPizzaria >nul 2>&1
taskkill /F /IM python.exe >nul 2>&1
timeout /t 2 /nobreak >nul

echo [2] Limpando portas...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8080') do (
    taskkill /F /PID %%a >nul 2>&1
)
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8000') do (
    taskkill /F /PID %%a >nul 2>&1
)

echo.
echo [3] Criando regra no Firewall...
netsh advfirewall firewall delete rule name="Django Pizzaria 8080" >nul 2>&1
netsh advfirewall firewall add rule name="Django Pizzaria 8080" dir=in action=allow protocol=TCP localport=8080

echo.
echo [4] Testando diferentes configuracoes...
echo ============================================
echo.

echo TESTE 1: Servidor em localhost:8080
echo ------------------------------------
echo Acesse: http://localhost:8080
echo         http://127.0.0.1:8080
echo.
echo Iniciando servidor (aguarde 10 segundos)...
echo.

start /B cmd /c "call .venv\Scripts\activate.bat && python manage.py runserver localhost:8080 2>&1"
timeout /t 10 /nobreak

echo.
echo Testando conexao...
curl -s -o nul -w "Status: %%{http_code}\n" http://localhost:8080 2>nul || echo FALHOU: localhost:8080
curl -s -o nul -w "Status: %%{http_code}\n" http://127.0.0.1:8080 2>nul || echo FALHOU: 127.0.0.1:8080

echo.
echo Parando servidor...
taskkill /F /IM python.exe >nul 2>&1
timeout /t 3 /nobreak >nul

echo.
echo ============================================
echo TESTE 2: Servidor em 127.0.0.1:8080
echo ------------------------------------
echo.

start /B cmd /c "call .venv\Scripts\activate.bat && python manage.py runserver 127.0.0.1:8080 2>&1"
timeout /t 10 /nobreak

echo Testando conexao...
curl -s -o nul -w "Status: %%{http_code}\n" http://localhost:8080 2>nul || echo FALHOU: localhost:8080
curl -s -o nul -w "Status: %%{http_code}\n" http://127.0.0.1:8080 2>nul || echo FALHOU: 127.0.0.1:8080

echo.
echo Parando servidor...
taskkill /F /IM python.exe >nul 2>&1
timeout /t 3 /nobreak >nul

echo.
echo ============================================
echo TESTE 3: Servidor em 0.0.0.0:8080
echo ------------------------------------
echo.

start /B cmd /c "call .venv\Scripts\activate.bat && python manage.py runserver 0.0.0.0:8080 2>&1"
timeout /t 10 /nobreak

echo Testando conexao...
curl -s -o nul -w "Status: %%{http_code}\n" http://localhost:8080 2>nul || echo FALHOU: localhost:8080
curl -s -o nul -w "Status: %%{http_code}\n" http://127.0.0.1:8080 2>nul || echo FALHOU: 127.0.0.1:8080

echo.
echo ============================================
echo.
echo Se nenhum teste funcionou, pode ser:
echo - Antivirus bloqueando
echo - Proxy configurado no navegador
echo - Problema com o virtual environment
echo.
echo SOLUCAO FINAL: Usar run_no_auth.py diretamente
echo.
pause

echo.
echo [5] Iniciando servidor FINAL com run_no_auth.py
echo ============================================
echo.
python run_no_auth.py