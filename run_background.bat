@echo off
REM Script para rodar o servidor Django em segundo plano no Windows
REM Usa o run_no_auth.py já existente

echo ========================================
echo   INICIANDO SERVIDOR EM SEGUNDO PLANO
echo ========================================
echo.

REM Ativa o ambiente virtual
call .venv\Scripts\activate.bat

REM Verifica se o Python está disponível
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Python não encontrado! Verifique se o ambiente virtual está ativo.
    pause
    exit /b 1
)

REM Mata processos anteriores na porta 8080
echo [1] Verificando processos na porta 8080...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8080 ^| findstr LISTENING') do (
    echo Finalizando processo PID: %%a
    taskkill /F /PID %%a >nul 2>&1
)

REM Cria pasta de logs se não existir
if not exist "logs" mkdir logs

REM Define arquivo de log com data/hora
set LOGFILE=logs\server_%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%%time:~6,2%.log
set LOGFILE=%LOGFILE: =0%

echo [2] Iniciando servidor Django em segundo plano...
echo    Log: %LOGFILE%
echo.

REM Inicia o servidor em segundo plano usando START
start /B "Django Server" cmd /c "python run_no_auth.py > %LOGFILE% 2>&1"

REM Aguarda um momento para o servidor iniciar
timeout /t 3 /nobreak >nul

REM Verifica se o servidor está rodando
netstat -an | findstr :8080 | findstr LISTENING >nul
if errorlevel 1 (
    echo [ERRO] Servidor não iniciou corretamente!
    echo Verifique o log em: %LOGFILE%
    pause
    exit /b 1
) else (
    echo [SUCESSO] Servidor rodando em segundo plano!
    echo.
    echo URLs disponíveis:
    echo   - http://localhost:8080
    echo   - http://127.0.0.1:8080
    echo.
    echo Para parar o servidor, use: stop_server.bat
    echo Para ver os logs: type %LOGFILE%
    echo.
)

REM Salva o PID do processo para poder parar depois
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8080 ^| findstr LISTENING') do (
    echo %%a > server.pid
    echo PID do servidor: %%a
)

echo.
echo Pressione qualquer tecla para fechar esta janela...
echo (O servidor continuará rodando em segundo plano)
pause >nul