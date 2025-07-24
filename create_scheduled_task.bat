@echo off
REM Script para criar Tarefa Agendada do Windows para manter servidor sempre rodando
REM Alternativa ao serviço Windows, mais simples de configurar

echo ============================================
echo   CRIAR TAREFA AGENDADA - DJANGO SERVER
echo ============================================
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

REM Configurações
set TASK_NAME=DjangoPizzariaAutoStart
set SCRIPT_PATH=%CD%\run_forever.bat

echo Este script criará uma tarefa agendada que:
echo.
echo 1. Inicia o servidor Django automaticamente no boot
echo 2. Reinicia o servidor se ele parar
echo 3. Mantém o servidor rodando 24/7
echo.
echo Deseja continuar? (S/N)
set /p CONFIRM=

if /i not "%CONFIRM%"=="S" (
    echo Operação cancelada.
    pause
    exit /b 0
)

echo.
echo [1] Removendo tarefa existente (se houver)...
schtasks /delete /tn "%TASK_NAME%" /f >nul 2>&1

echo.
echo [2] Criando nova tarefa agendada...

REM Cria arquivo XML temporário com a configuração da tarefa
set XML_FILE=%TEMP%\django_task.xml
(
echo ^<?xml version="1.0" encoding="UTF-16"?^>
echo ^<Task version="1.4" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task"^>
echo   ^<RegistrationInfo^>
echo     ^<Date^>%date%^</Date^>
echo     ^<Author^>%USERNAME%^</Author^>
echo     ^<Description^>Mantém o servidor Django da pizzaria sempre rodando^</Description^>
echo   ^</RegistrationInfo^>
echo   ^<Triggers^>
echo     ^<BootTrigger^>
echo       ^<Enabled^>true^</Enabled^>
echo       ^<Delay^>PT30S^</Delay^>
echo     ^</BootTrigger^>
echo     ^<LogonTrigger^>
echo       ^<Enabled^>true^</Enabled^>
echo       ^<Delay^>PT10S^</Delay^>
echo     ^</LogonTrigger^>
echo   ^</Triggers^>
echo   ^<Principals^>
echo     ^<Principal id="Author"^>
echo       ^<UserId^>%USERDOMAIN%\%USERNAME%^</UserId^>
echo       ^<LogonType^>InteractiveToken^</LogonType^>
echo       ^<RunLevel^>HighestAvailable^</RunLevel^>
echo     ^</Principal^>
echo   ^</Principals^>
echo   ^<Settings^>
echo     ^<MultipleInstancesPolicy^>IgnoreNew^</MultipleInstancesPolicy^>
echo     ^<DisallowStartIfOnBatteries^>false^</DisallowStartIfOnBatteries^>
echo     ^<StopIfGoingOnBatteries^>false^</StopIfGoingOnBatteries^>
echo     ^<AllowHardTerminate^>false^</AllowHardTerminate^>
echo     ^<StartWhenAvailable^>true^</StartWhenAvailable^>
echo     ^<RunOnlyIfNetworkAvailable^>false^</RunOnlyIfNetworkAvailable^>
echo     ^<IdleSettings^>
echo       ^<StopOnIdleEnd^>false^</StopOnIdleEnd^>
echo       ^<RestartOnIdle^>false^</RestartOnIdle^>
echo     ^</IdleSettings^>
echo     ^<AllowStartOnDemand^>true^</AllowStartOnDemand^>
echo     ^<Enabled^>true^</Enabled^>
echo     ^<Hidden^>false^</Hidden^>
echo     ^<RunOnlyIfIdle^>false^</RunOnlyIfIdle^>
echo     ^<DisallowStartOnRemoteAppSession^>false^</DisallowStartOnRemoteAppSession^>
echo     ^<UseUnifiedSchedulingEngine^>true^</UseUnifiedSchedulingEngine^>
echo     ^<WakeToRun^>false^</WakeToRun^>
echo     ^<ExecutionTimeLimit^>PT0S^</ExecutionTimeLimit^>
echo     ^<Priority^>7^</Priority^>
echo     ^<RestartOnFailure^>
echo       ^<Interval^>PT1M^</Interval^>
echo       ^<Count^>999^</Count^>
echo     ^</RestartOnFailure^>
echo   ^</Settings^>
echo   ^<Actions Context="Author"^>
echo     ^<Exec^>
echo       ^<Command^>cmd.exe^</Command^>
echo       ^<Arguments^>/c "%SCRIPT_PATH%"^</Arguments^>
echo       ^<WorkingDirectory^>%CD%^</WorkingDirectory^>
echo     ^</Exec^>
echo   ^</Actions^>
echo ^</Task^>
) > "%XML_FILE%"

REM Importa a tarefa
schtasks /create /xml "%XML_FILE%" /tn "%TASK_NAME%"

REM Remove arquivo temporário
del "%XML_FILE%"

if errorlevel 1 (
    echo.
    echo [ERRO] Falha ao criar tarefa agendada!
    pause
    exit /b 1
)

echo.
echo [3] Tarefa agendada criada com sucesso!
echo.

REM Menu de opções
:MENU
echo ============================================
echo   GERENCIAR TAREFA AGENDADA
echo ============================================
echo.
echo [1] Iniciar Tarefa Agora
echo [2] Parar Tarefa
echo [3] Ver Status da Tarefa
echo [4] Desabilitar Tarefa
echo [5] Habilitar Tarefa
echo [6] Remover Tarefa
echo [7] Sair
echo.
set /p OPTION="Escolha uma opção: "

if "%OPTION%"=="1" goto START_TASK
if "%OPTION%"=="2" goto STOP_TASK
if "%OPTION%"=="3" goto STATUS_TASK
if "%OPTION%"=="4" goto DISABLE_TASK
if "%OPTION%"=="5" goto ENABLE_TASK
if "%OPTION%"=="6" goto REMOVE_TASK
if "%OPTION%"=="7" exit /b 0
goto MENU

:START_TASK
echo.
schtasks /run /tn "%TASK_NAME%"
echo.
pause
goto MENU

:STOP_TASK
echo.
schtasks /end /tn "%TASK_NAME%"
echo.
REM Também mata o processo do servidor
taskkill /F /FI "WINDOWTITLE eq SERVIDOR DJANGO - MODO FOREVER" >nul 2>&1
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8080 ^| findstr LISTENING') do (
    taskkill /F /PID %%a >nul 2>&1
)
echo Tarefa parada!
echo.
pause
goto MENU

:STATUS_TASK
echo.
schtasks /query /tn "%TASK_NAME%" /v
echo.
pause
goto MENU

:DISABLE_TASK
echo.
schtasks /change /tn "%TASK_NAME%" /disable
echo Tarefa desabilitada!
echo.
pause
goto MENU

:ENABLE_TASK
echo.
schtasks /change /tn "%TASK_NAME%" /enable
echo Tarefa habilitada!
echo.
pause
goto MENU

:REMOVE_TASK
echo.
set /p CONFIRM="Tem certeza que deseja remover a tarefa? (S/N): "
if /i "%CONFIRM%"=="S" (
    schtasks /delete /tn "%TASK_NAME%" /f
    echo Tarefa removida!
) else (
    echo Operação cancelada.
)
echo.
pause
goto MENU