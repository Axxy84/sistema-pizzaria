@echo off
REM Script simplificado para instalar Django como Serviço Windows com NSSM
REM Coloque o nssm.exe na mesma pasta deste script ou na pasta tools

echo ============================================
echo   INSTALADOR RAPIDO - SERVICO DJANGO
echo ============================================
echo.

REM Verifica se está rodando como Administrador
net session >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Execute como ADMINISTRADOR!
    echo.
    echo Clique com botao direito neste arquivo e
    echo selecione "Executar como Administrador"
    echo.
    pause
    exit /b 1
)

REM Procura o NSSM
set NSSM_PATH=
if exist "nssm.exe" (
    set NSSM_PATH=nssm.exe
) else if exist "tools\nssm.exe" (
    set NSSM_PATH=tools\nssm.exe
) else if exist "nssm-2.24\win64\nssm.exe" (
    set NSSM_PATH=nssm-2.24\win64\nssm.exe
    echo Copiando NSSM para pasta tools...
    if not exist "tools" mkdir tools
    copy "nssm-2.24\win64\nssm.exe" "tools\" >nul
    set NSSM_PATH=tools\nssm.exe
) else (
    echo [ERRO] NSSM.EXE nao encontrado!
    echo.
    echo Certifique-se de que o nssm.exe esta em uma destas pastas:
    echo - Na mesma pasta deste script
    echo - Na pasta "tools"
    echo - Na pasta "nssm-2.24\win64"
    echo.
    pause
    exit /b 1
)

echo [OK] NSSM encontrado em: %NSSM_PATH%
echo.

REM Configurações
set SERVICE_NAME=DjangoPizzaria
set PYTHON_EXE=%CD%\.venv\Scripts\python.exe
set SCRIPT_PATH=%CD%\run_no_auth.py

REM Verifica se o Python existe
if not exist "%PYTHON_EXE%" (
    echo [ERRO] Python nao encontrado em: %PYTHON_EXE%
    echo.
    echo Verifique se o ambiente virtual esta criado corretamente.
    echo.
    pause
    exit /b 1
)

echo ============================================
echo   CONFIGURACAO DO SERVICO
echo ============================================
echo.
echo Nome do Servico: %SERVICE_NAME%
echo Python: %PYTHON_EXE%
echo Script: %SCRIPT_PATH%
echo Pasta: %CD%
echo.
echo Deseja instalar o servico? (S/N)
set /p CONFIRM=

if /i not "%CONFIRM%"=="S" (
    echo.
    echo Instalacao cancelada.
    pause
    exit /b 0
)

echo.
echo [1] Removendo servico antigo (se existir)...
%NSSM_PATH% stop %SERVICE_NAME% >nul 2>&1
%NSSM_PATH% remove %SERVICE_NAME% confirm >nul 2>&1

echo.
echo [2] Instalando novo servico...
%NSSM_PATH% install %SERVICE_NAME% "%PYTHON_EXE%" "%SCRIPT_PATH%"

if errorlevel 1 (
    echo.
    echo [ERRO] Falha ao instalar servico!
    pause
    exit /b 1
)

echo.
echo [3] Configurando servico...

REM Nome de exibição
%NSSM_PATH% set %SERVICE_NAME% DisplayName "Django Pizzaria Server"

REM Descrição
%NSSM_PATH% set %SERVICE_NAME% Description "Sistema de Gestao de Pizzaria - Servidor Django"

REM Diretório de trabalho
%NSSM_PATH% set %SERVICE_NAME% AppDirectory "%CD%"

REM Iniciar automaticamente
%NSSM_PATH% set %SERVICE_NAME% Start SERVICE_AUTO_START

REM Criar pasta de logs
if not exist "logs\service" mkdir "logs\service"

REM Configurar logs
%NSSM_PATH% set %SERVICE_NAME% AppStdout "%CD%\logs\service\servico.log"
%NSSM_PATH% set %SERVICE_NAME% AppStderr "%CD%\logs\service\erro.log"
%NSSM_PATH% set %SERVICE_NAME% AppRotateFiles 1
%NSSM_PATH% set %SERVICE_NAME% AppRotateOnline 1
%NSSM_PATH% set %SERVICE_NAME% AppRotateBytes 10485760

REM Reiniciar se falhar
%NSSM_PATH% set %SERVICE_NAME% AppThrottle 3000
%NSSM_PATH% set %SERVICE_NAME% AppExit Default Restart
%NSSM_PATH% set %SERVICE_NAME% AppRestartDelay 5000

echo.
echo [4] Iniciando servico...
net start %SERVICE_NAME%

if errorlevel 1 (
    echo.
    echo [AVISO] Servico instalado mas nao iniciou automaticamente.
    echo Use o comando: net start %SERVICE_NAME%
) else (
    echo.
    echo ============================================
    echo   SUCESSO! SERVICO INSTALADO E RODANDO
    echo ============================================
)

echo.
echo COMANDOS UTEIS:
echo.
echo Parar servico:    net stop %SERVICE_NAME%
echo Iniciar servico:  net start %SERVICE_NAME%
echo Status:           sc query %SERVICE_NAME%
echo Desinstalar:      %NSSM_PATH% remove %SERVICE_NAME%
echo.
echo O servidor agora:
echo - Inicia automaticamente com o Windows
echo - Reinicia se houver falha
echo - Roda em background 24/7
echo.
echo Acesse: http://localhost:8080
echo.
echo Logs salvos em: logs\service\
echo.
pause