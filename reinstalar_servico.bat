@echo off
echo ============================================
echo   REINSTALAR SERVICO WINDOWS
echo ============================================
echo.

REM Para e remove servico antigo
echo [1] Removendo servico antigo...
net stop DjangoPizzaria >nul 2>&1
sc delete DjangoPizzaria >nul 2>&1

REM Procura NSSM
set NSSM_PATH=
if exist "nssm.exe" set NSSM_PATH=nssm.exe
if exist "tools\nssm.exe" set NSSM_PATH=tools\nssm.exe

if "%NSSM_PATH%"=="" (
    echo [ERRO] NSSM nao encontrado!
    pause
    exit /b 1
)

echo [2] Instalando servico novo...

REM Instala servico para executar manage.py diretamente
%NSSM_PATH% install DjangoPizzaria "%CD%\.venv\Scripts\python.exe" "%CD%\manage.py runserver 0.0.0.0:8080"

REM Configura
%NSSM_PATH% set DjangoPizzaria DisplayName "Django Pizzaria Server"
%NSSM_PATH% set DjangoPizzaria Description "Sistema de Gestao de Pizzaria"
%NSSM_PATH% set DjangoPizzaria AppDirectory "%CD%"
%NSSM_PATH% set DjangoPizzaria Start SERVICE_AUTO_START

REM Logs
if not exist "logs\service" mkdir "logs\service"
%NSSM_PATH% set DjangoPizzaria AppStdout "%CD%\logs\service\output.log"
%NSSM_PATH% set DjangoPizzaria AppStderr "%CD%\logs\service\error.log"

REM Variaveis de ambiente
%NSSM_PATH% set DjangoPizzaria AppEnvironmentExtra "PYTHONUNBUFFERED=1" "DJANGO_SETTINGS_MODULE=DjangoProject.settings"

REM Restart automatico
%NSSM_PATH% set DjangoPizzaria AppExit Default Restart
%NSSM_PATH% set DjangoPizzaria AppRestartDelay 5000

echo.
echo [3] Iniciando servico...
net start DjangoPizzaria

echo.
echo [4] Aguardando servidor iniciar...
timeout /t 5 /nobreak

echo.
echo [5] Verificando...
netstat -an | findstr :8080 | findstr LISTENING
if errorlevel 1 (
    echo.
    echo [ERRO] Servidor nao esta escutando na porta 8080!
    echo Verifique os logs em: logs\service\
) else (
    echo.
    echo [SUCESSO] Servidor rodando!
    echo Acesse: http://localhost:8080
)

echo.
pause