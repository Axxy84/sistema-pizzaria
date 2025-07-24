@echo off
REM Script para corrigir problemas comuns do serviço

echo ============================================
echo   CORRIGIR SERVICO DJANGO
echo ============================================
echo.

REM Para o serviço primeiro
echo [1] Parando servico...
net stop DjangoPizzaria >nul 2>&1

REM Limpa logs antigos
echo [2] Limpando logs antigos...
if exist "logs\service\servico.log" del "logs\service\servico.log"
if exist "logs\service\erro.log" del "logs\service\erro.log"

REM Mata processos Python travados
echo [3] Finalizando processos Python travados...
taskkill /F /IM python.exe >nul 2>&1

REM Verifica portas travadas
echo [4] Liberando porta 8080...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8080 ^| findstr LISTENING') do (
    echo Finalizando processo PID: %%a
    taskkill /F /PID %%a >nul 2>&1
)

REM Reconfigura o serviço para usar cmd wrapper
echo [5] Reconfigurando servico...

REM Cria um wrapper batch
echo @echo off > run_service_wrapper.bat
echo cd /d "%CD%" >> run_service_wrapper.bat
echo call .venv\Scripts\activate.bat >> run_service_wrapper.bat
echo python run_no_auth.py >> run_service_wrapper.bat

REM Procura NSSM
set NSSM_PATH=
if exist "nssm.exe" set NSSM_PATH=nssm.exe
if exist "tools\nssm.exe" set NSSM_PATH=tools\nssm.exe

if "%NSSM_PATH%"=="" (
    echo [ERRO] NSSM nao encontrado!
    pause
    exit /b 1
)

REM Reconfigura para usar o wrapper
%NSSM_PATH% set DjangoPizzaria Application "%CD%\run_service_wrapper.bat"
%NSSM_PATH% set DjangoPizzaria AppDirectory "%CD%"

REM Adiciona variável de ambiente
%NSSM_PATH% set DjangoPizzaria AppEnvironmentExtra "PYTHONUNBUFFERED=1"

REM Configura para mostrar console (para debug)
%NSSM_PATH% set DjangoPizzaria AppNoConsole 0

echo.
echo [6] Iniciando servico corrigido...
net start DjangoPizzaria

echo.
echo [7] Aguardando servidor iniciar...
timeout /t 5 /nobreak

echo.
echo [8] Testando conexao...
curl -s -o nul -w "Status HTTP: %%{http_code}\n" http://localhost:8080

echo.
echo ============================================
echo.
echo Se ainda nao funcionar, execute:
echo   verificar_servico.bat
echo.
echo Para ver logs em tempo real:
echo   type logs\service\servico.log
echo.
pause