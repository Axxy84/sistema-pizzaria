@echo off
echo ============================================
echo   ADICIONAR SERVIDOR NA INICIALIZACAO DO WINDOWS
echo ============================================
echo.
echo EXECUTE COMO ADMINISTRADOR!
echo.

echo [1] Criando pasta para scripts de inicializacao...
if not exist "C:\ProgramData\DjangoPizzaria" mkdir "C:\ProgramData\DjangoPizzaria"

echo.
echo [2] Copiando arquivos necessarios...
copy "%CD%\servidor_simples.py" "C:\ProgramData\DjangoPizzaria\" >nul
copy "%CD%\.env" "C:\ProgramData\DjangoPizzaria\" >nul 2>&1

echo.
echo [3] Criando script de inicializacao...
(
echo @echo off
echo cd /d "%CD%"
echo call .venv\Scripts\activate.bat
echo start /B python manage.py runserver 0.0.0.0:8080
) > "C:\ProgramData\DjangoPizzaria\iniciar_django.bat"

echo.
echo [4] Criando tarefa agendada...
echo.

REM Remove tarefa antiga se existir
schtasks /delete /tn "DjangoPizzariaStartup" /f >nul 2>&1

REM Cria nova tarefa
schtasks /create /tn "DjangoPizzariaStartup" /tr "C:\ProgramData\DjangoPizzaria\iniciar_django.bat" /sc onstart /ru "%USERNAME%" /rl highest /f

echo.
echo [5] Configurando a tarefa...
schtasks /change /tn "DjangoPizzariaStartup" /ri 1 /du 24:00

echo.
echo [6] Adicionando ao registro do Windows...
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run" /v "DjangoPizzaria" /t REG_SZ /d "C:\ProgramData\DjangoPizzaria\iniciar_django.bat" /f

echo.
echo ============================================
echo   INSTALACAO CONCLUIDA!
echo ============================================
echo.
echo O servidor sera iniciado automaticamente:
echo - Na proxima inicializacao do Windows
echo - Rodando em segundo plano
echo - Na porta 8080
echo.
echo Para testar agora:
echo schtasks /run /tn "DjangoPizzariaStartup"
echo.
echo Para remover da inicializacao:
echo - Execute: remover_inicializacao.bat
echo.
pause