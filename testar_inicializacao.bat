@echo off
echo ============================================
echo   TESTANDO INICIALIZACAO AUTOMATICA
echo ============================================
echo.

echo [1] Verificando processos Python...
tasklist | findstr python
echo.

echo [2] Verificando porta 8080...
netstat -an | findstr :8080 | findstr LISTENING
echo.

echo [3] Testando tarefa agendada...
echo Executando tarefa...
schtasks /run /tn "DjangoPizzaria_Startup"
echo.
echo Aguardando 5 segundos...
timeout /t 5 /nobreak >nul
echo.
echo Verificando novamente...
netstat -an | findstr :8080 | findstr LISTENING
echo.

echo [4] Status do servico Windows...
sc query DjangoPizzariaAuto | findstr "STATE"
echo.

echo [5] Tentando iniciar servico...
net start DjangoPizzariaAuto 2>&1
echo.

echo [6] Verificando se servidor esta acessivel...
echo.
curl -s -o nul -w "localhost:8080 - Status: %%{http_code}\n" http://localhost:8080 2>nul
curl -s -o nul -w "127.0.0.1:8080 - Status: %%{http_code}\n" http://127.0.0.1:8080 2>nul
echo.

echo ============================================
echo Se o servidor estiver rodando, voce vera:
echo - Processo python.exe na lista
echo - Porta 8080 LISTENING
echo - Status HTTP 200 ou 302
echo ============================================
echo.
pause