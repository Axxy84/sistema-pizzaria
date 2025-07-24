@echo off
echo ============================================
echo   REMOVER SERVIDOR DA INICIALIZACAO
echo ============================================
echo.
echo EXECUTE COMO ADMINISTRADOR!
echo.

echo [1] Removendo tarefa agendada...
schtasks /delete /tn "DjangoPizzariaStartup" /f

echo.
echo [2] Removendo do registro...
reg delete "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run" /v "DjangoPizzaria" /f

echo.
echo [3] Parando processos...
taskkill /F /IM python.exe >nul 2>&1

echo.
echo [4] Removendo arquivos...
if exist "C:\ProgramData\DjangoPizzaria" (
    rmdir /s /q "C:\ProgramData\DjangoPizzaria"
)

echo.
echo ============================================
echo   REMOCAO CONCLUIDA!
echo ============================================
echo.
echo O servidor nao sera mais iniciado automaticamente.
echo.
pause