@echo off
REM Script avançado para rodar servidor Django como um serviço persistente no Windows
REM Com monitoramento, auto-restart e notificações

setlocal enabledelayedexpansion

echo ============================================
echo   DJANGO SERVER - SERVICO PERSISTENTE
echo ============================================
echo.

REM Configurações
set SERVER_NAME=DjangoPizzaria
set PORT=8080
set RESTART_DELAY=3
set CHECK_INTERVAL=10
set LOG_DIR=logs\service
set PYTHON_PATH=.venv\Scripts\python.exe
set SERVER_SCRIPT=run_no_auth.py

REM Cria diretórios necessários
if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"

REM Arquivo de configuração
set CONFIG_FILE=%LOG_DIR%\service_config.txt
set PID_FILE=%LOG_DIR%\server.pid
set STATUS_FILE=%LOG_DIR%\server.status

REM Ativa ambiente virtual
call .venv\Scripts\activate.bat

REM Função principal
:MAIN_MENU
cls
echo ============================================
echo   DJANGO SERVER - SERVICO PERSISTENTE
echo ============================================
echo.
echo [1] Iniciar Serviço
echo [2] Status do Serviço
echo [3] Parar Serviço
echo [4] Ver Logs
echo [5] Configurações
echo [6] Sair
echo.
set /p OPTION="Escolha uma opção: "

if "%OPTION%"=="1" goto START_SERVICE
if "%OPTION%"=="2" goto CHECK_STATUS
if "%OPTION%"=="3" goto STOP_SERVICE
if "%OPTION%"=="4" goto VIEW_LOGS
if "%OPTION%"=="5" goto SETTINGS
if "%OPTION%"=="6" exit /b 0
goto MAIN_MENU

:START_SERVICE
cls
echo ============================================
echo   INICIANDO SERVICO PERSISTENTE
echo ============================================
echo.

REM Verifica se já está rodando
call :CHECK_IF_RUNNING
if %errorlevel%==0 (
    echo [AVISO] O serviço já está em execução!
    echo.
    pause
    goto MAIN_MENU
)

REM Inicia o monitor em background
echo [1] Iniciando monitor de serviço...
start /B /MIN cmd /c "%~f0" MONITOR

echo [2] Serviço iniciado com sucesso!
echo.
echo O servidor está rodando em modo persistente.
echo Ele será reiniciado automaticamente em caso de falha.
echo.
pause
goto MAIN_MENU

:MONITOR
REM Loop infinito de monitoramento
title %SERVER_NAME% - Monitor de Serviço

:MONITOR_LOOP
REM Verifica se o servidor está rodando
netstat -an | findstr :%PORT% | findstr LISTENING >nul
if errorlevel 1 (
    REM Servidor não está rodando, inicia
    call :START_SERVER_INTERNAL
)

REM Aguarda antes de verificar novamente
timeout /t %CHECK_INTERVAL% /nobreak >nul 2>&1
goto MONITOR_LOOP

:START_SERVER_INTERNAL
REM Registra o restart
echo [%date% %time%] Iniciando servidor... >> "%LOG_DIR%\monitor.log"

REM Define arquivo de log
set CURRENT_LOG=%LOG_DIR%\server_%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%%time:~6,2%.log
set CURRENT_LOG=!CURRENT_LOG: =0!

REM Mata processos antigos
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :%PORT% ^| findstr LISTENING') do (
    taskkill /F /PID %%a >nul 2>&1
)

REM Inicia o servidor
start /B cmd /c "%PYTHON_PATH% %SERVER_SCRIPT% > "!CURRENT_LOG!" 2>&1"

REM Aguarda o servidor iniciar
timeout /t %RESTART_DELAY% /nobreak >nul

REM Verifica se iniciou
netstat -an | findstr :%PORT% | findstr LISTENING >nul
if errorlevel 1 (
    echo [%date% %time%] ERRO: Servidor não iniciou! >> "%LOG_DIR%\monitor.log"
) else (
    echo [%date% %time%] Servidor iniciado com sucesso >> "%LOG_DIR%\monitor.log"
    REM Salva o PID
    for /f "tokens=5" %%a in ('netstat -aon ^| findstr :%PORT% ^| findstr LISTENING') do (
        echo %%a > "%PID_FILE%"
    )
)
exit /b

:CHECK_STATUS
cls
echo ============================================
echo   STATUS DO SERVICO
echo ============================================
echo.

call :CHECK_IF_RUNNING
if %errorlevel%==0 (
    echo Status: [RODANDO]
    echo.
    if exist "%PID_FILE%" (
        set /p PID=<"%PID_FILE%"
        echo PID: !PID!
    )
    echo Porta: %PORT%
    echo.
    echo Testando conexão...
    curl -s -o nul -w "HTTP Status: %%{http_code}\n" http://localhost:%PORT% 2>nul
) else (
    echo Status: [PARADO]
)

echo.
echo ============================================
echo.

REM Mostra últimas linhas do log do monitor
if exist "%LOG_DIR%\monitor.log" (
    echo Últimas atividades:
    echo.
    type "%LOG_DIR%\monitor.log" | more +eof-10
)

echo.
pause
goto MAIN_MENU

:STOP_SERVICE
cls
echo ============================================
echo   PARANDO SERVICO
echo ============================================
echo.

REM Para o monitor
echo [1] Parando monitor...
taskkill /F /FI "WINDOWTITLE eq %SERVER_NAME% - Monitor de Serviço" >nul 2>&1

REM Para o servidor
echo [2] Parando servidor...
if exist "%PID_FILE%" (
    set /p PID=<"%PID_FILE%"
    taskkill /F /PID !PID! >nul 2>&1
    del "%PID_FILE%"
)

REM Para qualquer processo na porta
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :%PORT% ^| findstr LISTENING') do (
    taskkill /F /PID %%a >nul 2>&1
)

echo [3] Serviço parado com sucesso!
echo.
pause
goto MAIN_MENU

:VIEW_LOGS
cls
echo ============================================
echo   LOGS DO SERVICO
echo ============================================
echo.
echo [1] Log do Monitor
echo [2] Último Log do Servidor
echo [3] Listar Todos os Logs
echo [4] Voltar
echo.
set /p LOG_OPTION="Escolha uma opção: "

if "%LOG_OPTION%"=="1" (
    if exist "%LOG_DIR%\monitor.log" (
        type "%LOG_DIR%\monitor.log" | more
    ) else (
        echo Nenhum log de monitor encontrado.
    )
    pause
)

if "%LOG_OPTION%"=="2" (
    for /f "delims=" %%i in ('dir /b /o-d "%LOG_DIR%\server_*.log" 2^>nul') do (
        type "%LOG_DIR%\%%i" | more
        goto :LOG_DONE
    )
    echo Nenhum log de servidor encontrado.
    :LOG_DONE
    pause
)

if "%LOG_OPTION%"=="3" (
    dir /b /o-d "%LOG_DIR%\*.log" 2>nul
    pause
)

goto VIEW_LOGS

:SETTINGS
cls
echo ============================================
echo   CONFIGURACOES DO SERVICO
echo ============================================
echo.
echo Porta: %PORT%
echo Intervalo de Verificação: %CHECK_INTERVAL% segundos
echo Delay de Restart: %RESTART_DELAY% segundos
echo Diretório de Logs: %LOG_DIR%
echo Python: %PYTHON_PATH%
echo Script: %SERVER_SCRIPT%
echo.
pause
goto MAIN_MENU

:CHECK_IF_RUNNING
REM Verifica se o servidor está rodando
netstat -an | findstr :%PORT% | findstr LISTENING >nul
exit /b %errorlevel%

REM Se foi chamado com parâmetro MONITOR, vai direto para o monitor
if "%1"=="MONITOR" goto MONITOR