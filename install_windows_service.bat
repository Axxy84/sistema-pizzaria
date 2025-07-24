@echo off
REM Script para instalar o Django como Serviço do Windows usando NSSM
REM NSSM = Non-Sucking Service Manager

echo ============================================
echo   INSTALADOR DE SERVICO WINDOWS
echo ============================================
echo.
echo Este script instalará o Django Server como
echo um Serviço do Windows que inicia automaticamente.
echo.

REM Verifica se está rodando como Administrador
net session >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Este script precisa ser executado como Administrador!
    echo.
    echo Clique com botão direito e selecione "Executar como Administrador"
    pause
    exit /b 1
)

REM Configurações do serviço
set SERVICE_NAME=DjangoPizzariaServer
set SERVICE_DISPLAY=Django Pizzaria Server
set SERVICE_DESCRIPTION=Servidor Django para Sistema de Pizzaria
set PYTHON_PATH=%CD%\.venv\Scripts\python.exe
set SCRIPT_PATH=%CD%\run_no_auth.py
set WORKING_DIR=%CD%

REM Verifica se o NSSM existe
if not exist "tools\nssm.exe" (
    echo [1] NSSM não encontrado. Baixando...
    echo.
    
    REM Cria pasta tools
    if not exist "tools" mkdir tools
    
    echo Por favor, baixe o NSSM manualmente:
    echo.
    echo 1. Acesse: https://nssm.cc/download
    echo 2. Baixe a versão mais recente (nssm-2.24.zip)
    echo 3. Extraia nssm.exe (versão 64-bit) para a pasta "tools"
    echo 4. Execute este script novamente
    echo.
    echo Ou use o PowerShell:
    echo.
    echo powershell -Command "Invoke-WebRequest -Uri 'https://nssm.cc/release/nssm-2.24.zip' -OutFile 'nssm.zip'; Expand-Archive -Path 'nssm.zip' -DestinationPath '.'; Copy-Item 'nssm-2.24\win64\nssm.exe' 'tools\'; Remove-Item -Recurse 'nssm-2.24', 'nssm.zip'"
    echo.
    pause
    exit /b 1
)

echo [1] NSSM encontrado!
echo.

REM Menu de opções
:MENU
echo Escolha uma opção:
echo.
echo [1] Instalar Serviço
echo [2] Remover Serviço
echo [3] Status do Serviço
echo [4] Iniciar Serviço
echo [5] Parar Serviço
echo [6] Reiniciar Serviço
echo [7] Configurar Serviço
echo [8] Sair
echo.
set /p OPTION="Digite a opção: "

if "%OPTION%"=="1" goto INSTALL
if "%OPTION%"=="2" goto REMOVE
if "%OPTION%"=="3" goto STATUS
if "%OPTION%"=="4" goto START
if "%OPTION%"=="5" goto STOP
if "%OPTION%"=="6" goto RESTART
if "%OPTION%"=="7" goto CONFIGURE
if "%OPTION%"=="8" exit /b 0
goto MENU

:INSTALL
echo.
echo [INSTALANDO SERVICO]
echo.

REM Remove serviço existente se houver
tools\nssm.exe remove %SERVICE_NAME% confirm >nul 2>&1

REM Instala o serviço
echo Instalando serviço %SERVICE_NAME%...
tools\nssm.exe install %SERVICE_NAME% "%PYTHON_PATH%" "%SCRIPT_PATH%"

REM Configura o serviço
tools\nssm.exe set %SERVICE_NAME% DisplayName "%SERVICE_DISPLAY%"
tools\nssm.exe set %SERVICE_NAME% Description "%SERVICE_DESCRIPTION%"
tools\nssm.exe set %SERVICE_NAME% AppDirectory "%WORKING_DIR%"
tools\nssm.exe set %SERVICE_NAME% Start SERVICE_AUTO_START

REM Configura logs
tools\nssm.exe set %SERVICE_NAME% AppStdout "%WORKING_DIR%\logs\service\stdout.log"
tools\nssm.exe set %SERVICE_NAME% AppStderr "%WORKING_DIR%\logs\service\stderr.log"
tools\nssm.exe set %SERVICE_NAME% AppRotateFiles 1
tools\nssm.exe set %SERVICE_NAME% AppRotateSeconds 86400
tools\nssm.exe set %SERVICE_NAME% AppRotateBytes 10485760

REM Configura restart automático
tools\nssm.exe set %SERVICE_NAME% AppThrottle 1500
tools\nssm.exe set %SERVICE_NAME% AppExit Default Restart
tools\nssm.exe set %SERVICE_NAME% AppRestartDelay 2000

REM Configura variáveis de ambiente
tools\nssm.exe set %SERVICE_NAME% AppEnvironmentExtra PYTHONUNBUFFERED=1

echo.
echo Serviço instalado com sucesso!
echo.
echo Iniciando serviço...
net start %SERVICE_NAME%

echo.
pause
goto MENU

:REMOVE
echo.
echo [REMOVENDO SERVICO]
echo.
set /p CONFIRM="Tem certeza que deseja remover o serviço? (S/N): "
if /i "%CONFIRM%"=="S" (
    net stop %SERVICE_NAME% >nul 2>&1
    tools\nssm.exe remove %SERVICE_NAME% confirm
    echo Serviço removido!
) else (
    echo Operação cancelada.
)
echo.
pause
goto MENU

:STATUS
echo.
echo [STATUS DO SERVICO]
echo.
sc query %SERVICE_NAME%
echo.

REM Verifica se está respondendo
echo Testando conexão com o servidor...
curl -s -o nul -w "HTTP Status: %%{http_code}\n" http://localhost:8080 2>nul
echo.
pause
goto MENU

:START
echo.
echo [INICIANDO SERVICO]
echo.
net start %SERVICE_NAME%
echo.
pause
goto MENU

:STOP
echo.
echo [PARANDO SERVICO]
echo.
net stop %SERVICE_NAME%
echo.
pause
goto MENU

:RESTART
echo.
echo [REINICIANDO SERVICO]
echo.
net stop %SERVICE_NAME%
timeout /t 2 /nobreak >nul
net start %SERVICE_NAME%
echo.
pause
goto MENU

:CONFIGURE
echo.
echo [CONFIGURAR SERVICO]
echo.
tools\nssm.exe edit %SERVICE_NAME%
echo.
pause
goto MENU