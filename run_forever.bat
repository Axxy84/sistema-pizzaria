@echo off
REM Script para manter o servidor Django SEMPRE rodando no Windows
REM Com auto-restart em caso de falha

echo ========================================
echo   SERVIDOR DJANGO - MODO FOREVER
echo ========================================
echo.
echo Este script manterá o servidor rodando permanentemente.
echo Ele reiniciará automaticamente em caso de falha.
echo.
echo Para parar, feche esta janela ou use Ctrl+C
echo ========================================
echo.

REM Ativa o ambiente virtual
call .venv\Scripts\activate.bat

REM Verifica se o Python está disponível
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Python não encontrado! Verifique se o ambiente virtual está ativo.
    pause
    exit /b 1
)

REM Cria pasta de logs se não existir
if not exist "logs" mkdir logs
if not exist "logs\forever" mkdir logs\forever

REM Define variáveis
set RESTART_COUNT=0
set MAX_RESTART_ATTEMPTS=1000000
set RESTART_DELAY=5

:START_SERVER
cls
echo ========================================
echo   SERVIDOR DJANGO - MODO FOREVER
echo ========================================
echo.
echo Iniciando servidor... (Tentativa #%RESTART_COUNT%)
echo.

REM Mata processos anteriores na porta 8080
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8080 ^| findstr LISTENING') do (
    taskkill /F /PID %%a >nul 2>&1
)

REM Define arquivo de log com data/hora
set LOGFILE=logs\forever\server_%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%%time:~6,2%.log
set LOGFILE=%LOGFILE: =0%

echo [%date% %time%] Iniciando servidor (Tentativa #%RESTART_COUNT%) >> logs\forever\restart_history.log
echo Log atual: %LOGFILE%
echo.

REM Inicia o servidor
echo ======================================== >> "%LOGFILE%"
echo INICIO DA SESSAO: %date% %time% >> "%LOGFILE%"
echo Tentativa #%RESTART_COUNT% >> "%LOGFILE%"
echo ======================================== >> "%LOGFILE%"
echo. >> "%LOGFILE%"

python run_no_auth.py >> "%LOGFILE%" 2>&1

REM Se chegou aqui, o servidor parou
echo.
echo [%date% %time%] SERVIDOR PAROU! Código de saída: %errorlevel% >> logs\forever\restart_history.log
echo.
echo [AVISO] Servidor parou! Reiniciando em %RESTART_DELAY% segundos...
echo Código de saída: %errorlevel%
echo.

REM Incrementa contador de restart
set /a RESTART_COUNT=%RESTART_COUNT%+1

REM Verifica se excedeu o limite (improvável, mas por segurança)
if %RESTART_COUNT% GTR %MAX_RESTART_ATTEMPTS% (
    echo [ERRO] Número máximo de tentativas excedido!
    echo Verifique os logs em: logs\forever\
    pause
    exit /b 1
)

REM Aguarda antes de reiniciar
timeout /t %RESTART_DELAY% /nobreak

REM Reinicia o servidor
goto START_SERVER