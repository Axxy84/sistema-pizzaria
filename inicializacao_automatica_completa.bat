@echo off
echo ============================================
echo   CONFIGURACAO COMPLETA DE INICIALIZACAO
echo ============================================
echo.
echo EXECUTE COMO ADMINISTRADOR!
echo.
echo Este script configura 3 metodos diferentes
echo para garantir que o servidor SEMPRE inicie
echo.

echo [1] METODO 1: Tarefa Agendada
echo ============================================
schtasks /delete /tn "DjangoPizzaria_Startup" /f >nul 2>&1
schtasks /create /tn "DjangoPizzaria_Startup" ^
  /tr "\"%CD%\servidor_background_vbs.vbs\"" ^
  /sc onstart ^
  /delay 0000:30 ^
  /rl highest ^
  /f

echo Tarefa criada: DjangoPizzaria_Startup
echo.

echo [2] METODO 2: Servico Windows com NSSM
echo ============================================
set NSSM_PATH=
if exist "nssm.exe" set NSSM_PATH=nssm.exe
if exist "tools\nssm.exe" set NSSM_PATH=tools\nssm.exe

if not "%NSSM_PATH%"=="" (
    echo Instalando servico com NSSM...
    %NSSM_PATH% install DjangoPizzariaAuto "%CD%\.venv\Scripts\python.exe" "%CD%\manage.py runserver 0.0.0.0:8080"
    %NSSM_PATH% set DjangoPizzariaAuto AppDirectory "%CD%"
    %NSSM_PATH% set DjangoPizzariaAuto Start SERVICE_AUTO_START
    %NSSM_PATH% set DjangoPizzariaAuto DisplayName "Django Pizzaria Auto"
    %NSSM_PATH% set DjangoPizzariaAuto Description "Sistema de Pizzaria - Inicializacao Automatica"
    echo Servico instalado: DjangoPizzariaAuto
) else (
    echo [!] NSSM nao encontrado - pulando servico
)
echo.

echo [3] METODO 3: Pasta Startup do Windows
echo ============================================
echo Criando atalho na pasta Startup...
powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\DjangoPizzaria.lnk'); $Shortcut.TargetPath = '%CD%\servidor_background_vbs.vbs'; $Shortcut.WorkingDirectory = '%CD%'; $Shortcut.IconLocation = '%SystemRoot%\System32\SHELL32.dll,13'; $Shortcut.Save()"

echo Atalho criado na pasta Startup
echo.

echo [4] METODO 4: Registro do Windows
echo ============================================
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "DjangoPizzaria" /t REG_SZ /d "\"%CD%\servidor_background_vbs.vbs\"" /f
echo Entrada adicionada ao registro
echo.

echo ============================================
echo   VERIFICANDO CONFIGURACOES
echo ============================================
echo.

echo Tarefa agendada:
schtasks /query /tn "DjangoPizzaria_Startup" 2>nul | findstr "DjangoPizzaria_Startup"

echo.
echo Servico Windows:
sc query DjangoPizzariaAuto 2>nul | findstr "STATE"

echo.
echo Pasta Startup:
if exist "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\DjangoPizzaria.lnk" (
    echo [OK] Atalho existe na pasta Startup
) else (
    echo [!] Atalho NAO encontrado
)

echo.
echo Registro:
reg query "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "DjangoPizzaria" 2>nul | findstr "DjangoPizzaria"

echo.
echo ============================================
echo   INSTALACAO CONCLUIDA!
echo ============================================
echo.
echo O servidor sera iniciado automaticamente de 4 formas:
echo 1. Tarefa Agendada (30s apos boot)
echo 2. Servico Windows (se NSSM disponivel)
echo 3. Pasta Startup do usuario
echo 4. Registro do Windows
echo.
echo Para testar agora:
echo   schtasks /run /tn "DjangoPizzaria_Startup"
echo.
echo Para remover tudo:
echo   Execute: remover_todas_inicializacoes.bat
echo.
pause