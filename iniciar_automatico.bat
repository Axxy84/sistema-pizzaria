@echo off
chcp 65001 > nul
title Configurar Inicialização Automática

echo ========================================
echo   CONFIGURAR INICIALIZAÇÃO AUTOMÁTICA
echo ========================================
echo.

:: Criar atalho na pasta Startup do Windows
set STARTUP_FOLDER=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup
set PROJECT_PATH=%~dp0

echo Criando atalho na pasta de inicialização...

:: Criar script VBS para criar o atalho
echo Set objShell = CreateObject("WScript.Shell") > temp_startup.vbs
echo Set objLink = objShell.CreateShortcut("%STARTUP_FOLDER%\Sistema Pizzaria.lnk") >> temp_startup.vbs
echo objLink.TargetPath = "%PROJECT_PATH%iniciar_pizzaria.bat" >> temp_startup.vbs
echo objLink.WorkingDirectory = "%PROJECT_PATH%" >> temp_startup.vbs
echo objLink.WindowStyle = 7 >> temp_startup.vbs
echo objLink.Description = "Iniciar Sistema Pizzaria automaticamente" >> temp_startup.vbs
echo objLink.Save >> temp_startup.vbs

:: Executar o script VBS
cscript //NoLogo temp_startup.vbs

:: Limpar arquivo temporário
del temp_startup.vbs

echo.
echo ✅ Sistema configurado para iniciar automaticamente!
echo.
echo O sistema será iniciado sempre que o Windows iniciar.
echo Para desativar, delete o atalho em:
echo %STARTUP_FOLDER%
echo.
pause