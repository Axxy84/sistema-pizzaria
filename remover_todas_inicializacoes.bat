@echo off
echo ============================================
echo   REMOVER TODAS AS INICIALIZACOES
echo ============================================
echo.
echo EXECUTE COMO ADMINISTRADOR!
echo.

echo [1] Parando processos Python...
taskkill /F /IM python.exe >nul 2>&1
timeout /t 2 /nobreak >nul

echo.
echo [2] Removendo Tarefa Agendada...
schtasks /delete /tn "DjangoPizzaria_Startup" /f >nul 2>&1
schtasks /delete /tn "DjangoPizzariaStartup" /f >nul 2>&1

echo.
echo [3] Removendo Servico Windows...
net stop DjangoPizzariaAuto >nul 2>&1
sc delete DjangoPizzariaAuto >nul 2>&1
net stop DjangoPizzaria >nul 2>&1
sc delete DjangoPizzaria >nul 2>&1

echo.
echo [4] Removendo da Pasta Startup...
del "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\DjangoPizzaria.lnk" >nul 2>&1

echo.
echo [5] Removendo do Registro...
reg delete "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "DjangoPizzaria" /f >nul 2>&1
reg delete "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run" /v "DjangoPizzaria" /f >nul 2>&1

echo.
echo [6] Limpando arquivos temporarios...
if exist "C:\ProgramData\DjangoPizzaria" (
    rmdir /s /q "C:\ProgramData\DjangoPizzaria" >nul 2>&1
)

echo.
echo ============================================
echo   REMOCAO CONCLUIDA!
echo ============================================
echo.
echo Todas as configuracoes de inicializacao foram removidas.
echo O servidor nao sera mais iniciado automaticamente.
echo.
pause