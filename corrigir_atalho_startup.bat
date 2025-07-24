@echo off
echo ============================================
echo   CORRIGIR ATALHO NA PASTA STARTUP
echo ============================================
echo.

echo [1] Criando atalho manualmente...
echo.

REM Criar arquivo VBS temporário para criar o atalho
(
echo Set objShell = CreateObject("WScript.Shell"^)
echo Set objShortcut = objShell.CreateShortcut("%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\DjangoPizzaria.lnk"^)
echo objShortcut.TargetPath = "%CD%\servidor_background_vbs.vbs"
echo objShortcut.WorkingDirectory = "%CD%"
echo objShortcut.Description = "Django Pizzaria - Servidor"
echo objShortcut.IconLocation = "%SystemRoot%\System32\SHELL32.dll,13"
echo objShortcut.Save
) > temp_create_shortcut.vbs

REM Executar o VBS
cscript //nologo temp_create_shortcut.vbs

REM Deletar arquivo temporário
del temp_create_shortcut.vbs

echo.
echo [2] Verificando se foi criado...
if exist "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\DjangoPizzaria.lnk" (
    echo [OK] Atalho criado com sucesso!
    echo Local: %APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\
) else (
    echo [ERRO] Falha ao criar atalho
)

echo.
echo [3] Listando conteudo da pasta Startup...
echo.
dir "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\" /b

echo.
echo ============================================
echo.
pause