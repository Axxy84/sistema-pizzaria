@echo off
chcp 65001 > nul
title Criar Atalhos - Sistema Pizzaria

echo Criando atalhos do Sistema Pizzaria...

:: Obter caminho da área de trabalho
set "desktop=%USERPROFILE%\Desktop"
set "projectDir=%~dp0"

:: Criar atalho para iniciar o sistema
powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%desktop%\Sistema Pizzaria.lnk'); $Shortcut.TargetPath = '%projectDir%iniciar_pizzaria.bat'; $Shortcut.WorkingDirectory = '%projectDir%'; $Shortcut.IconLocation = '%windir%\System32\shell32.dll,17'; $Shortcut.Description = 'Iniciar Sistema Pizzaria'; $Shortcut.Save()"

:: Criar atalho para o navegador
powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%desktop%\Pizzaria - Navegador.lnk'); $Shortcut.TargetPath = '%ProgramFiles%\Google\Chrome\Application\chrome.exe'; $Shortcut.Arguments = 'http://localhost:8000'; $Shortcut.IconLocation = '%ProgramFiles%\Google\Chrome\Application\chrome.exe,0'; $Shortcut.Description = 'Abrir Sistema Pizzaria no Chrome'; $Shortcut.Save()"

:: Criar atalho para admin
powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%desktop%\Pizzaria - Admin.lnk'); $Shortcut.TargetPath = '%ProgramFiles%\Google\Chrome\Application\chrome.exe'; $Shortcut.Arguments = 'http://localhost:8000/admin'; $Shortcut.IconLocation = '%windir%\System32\shell32.dll,21'; $Shortcut.Description = 'Área Administrativa'; $Shortcut.Save()"

:: Criar atalho para pasta do projeto
powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%desktop%\Pizzaria - Arquivos.lnk'); $Shortcut.TargetPath = '%projectDir%'; $Shortcut.IconLocation = '%windir%\System32\shell32.dll,3'; $Shortcut.Description = 'Pasta do Sistema Pizzaria'; $Shortcut.Save()"

echo.
echo [✓] Atalhos criados com sucesso na área de trabalho!
echo.
echo Atalhos criados:
echo - Sistema Pizzaria (iniciar servidor)
echo - Pizzaria - Navegador (abrir no Chrome)
echo - Pizzaria - Admin (área administrativa)
echo - Pizzaria - Arquivos (pasta do sistema)
echo.
timeout /t 3 >nul