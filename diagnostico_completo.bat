@echo off
REM Script melhorado para diagnóstico completo

echo ============================================
echo   DIAGNOSTICO COMPLETO - DJANGO SERVER
echo ============================================
echo.

echo [1] Status do Servico:
echo --------------------------------------------
sc query DjangoPizzaria
echo.

echo [2] Verificando porta 8080:
echo --------------------------------------------
netstat -an | findstr :8080
if errorlevel 1 (
    echo Porta 8080 LIVRE - Nenhum processo escutando
) else (
    echo Porta 8080 EM USO - Processos:
    for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8080 ^| findstr LISTENING') do (
        echo PID: %%a
        for /f "tokens=1" %%b in ('tasklist /FI "PID eq %%a" ^| findstr %%a') do echo Processo: %%b
    )
)
echo.

echo [3] Verificando logs do servico:
echo --------------------------------------------
cd /d "%~dp0"

if exist "logs\service\servico.log" (
    echo === CONTEUDO DE servico.log ===
    type "logs\service\servico.log"
    echo.
    echo === FIM DO LOG ===
) else (
    echo [!] Arquivo logs\service\servico.log NAO encontrado
    echo Criando pasta de logs...
    if not exist "logs\service" mkdir "logs\service"
)
echo.

if exist "logs\service\erro.log" (
    echo === CONTEUDO DE erro.log ===
    type "logs\service\erro.log"
    echo.
    echo === FIM DO LOG ===
) else (
    echo [!] Arquivo logs\service\erro.log NAO encontrado
)
echo.

echo [4] Verificando ambiente Python:
echo --------------------------------------------
if exist ".venv\Scripts\python.exe" (
    echo [OK] Python encontrado em .venv
    call .venv\Scripts\activate.bat
    python --version
    where python
) else (
    echo [ERRO] Python NAO encontrado em .venv\Scripts\
    echo Verifique se o ambiente virtual esta correto
)
echo.

echo [5] Verificando arquivo run_no_auth.py:
echo --------------------------------------------
if exist "run_no_auth.py" (
    echo [OK] Arquivo run_no_auth.py encontrado
    echo Tamanho: 
    for %%A in (run_no_auth.py) do echo %%~zA bytes
) else (
    echo [ERRO] Arquivo run_no_auth.py NAO encontrado!
    echo.
    echo Arquivos Python na pasta:
    dir /b *.py
)
echo.

echo [6] Testando conexao com banco de dados:
echo --------------------------------------------
if exist ".env" (
    echo [OK] Arquivo .env encontrado
) else (
    echo [!] Arquivo .env NAO encontrado
    if exist ".env.example" (
        echo Copie .env.example para .env e configure
    )
)
echo.

pause