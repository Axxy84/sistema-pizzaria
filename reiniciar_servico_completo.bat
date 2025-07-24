@echo off
REM Script para reiniciar completamente o serviço Django

echo ============================================
echo   REINICIAR SERVICO DJANGO COMPLETO
echo ============================================
echo.

REM Para o serviço em qualquer estado
echo [1] Parando servico (estava pausado)...
sc stop DjangoPizzaria >nul 2>&1
timeout /t 2 /nobreak >nul

REM Mata qualquer processo Python
echo [2] Finalizando processos Python...
taskkill /F /IM python.exe >nul 2>&1

REM Limpa porta 8080
echo [3] Liberando porta 8080...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8080') do (
    taskkill /F /PID %%a >nul 2>&1
)

REM Cria estrutura de logs
echo [4] Criando estrutura de logs...
if not exist "logs" mkdir "logs"
if not exist "logs\service" mkdir "logs\service"

REM Limpa logs antigos para novo teste
echo [5] Limpando logs antigos...
if exist "logs\service\servico.log" (
    copy "logs\service\servico.log" "logs\service\servico_old.log" >nul
    del "logs\service\servico.log"
)
if exist "logs\service\erro.log" (
    copy "logs\service\erro.log" "logs\service\erro_old.log" >nul
    del "logs\service\erro.log"
)

REM Testa execução direta primeiro
echo [6] Testando execucao direta (5 segundos)...
echo.
call .venv\Scripts\activate.bat
start /B cmd /c "python run_no_auth.py > test_output.txt 2>&1"
timeout /t 5 /nobreak

REM Verifica se funcionou
netstat -an | findstr :8080 | findstr LISTENING >nul
if errorlevel 1 (
    echo [ERRO] Servidor nao iniciou no teste direto!
    echo.
    echo Verificando erro:
    if exist "test_output.txt" type test_output.txt
    echo.
    taskkill /F /IM python.exe >nul 2>&1
    pause
    exit /b 1
) else (
    echo [OK] Teste direto funcionou! Porta 8080 ativa.
    taskkill /F /IM python.exe >nul 2>&1
)

echo.
echo [7] Iniciando servico...
net start DjangoPizzaria

if errorlevel 1 (
    echo.
    echo [ERRO] Falha ao iniciar servico!
    echo Verifique os logs em: logs\service\
) else (
    echo.
    echo [8] Aguardando servico iniciar...
    timeout /t 5 /nobreak
    
    echo.
    echo [9] Verificando status final...
    sc query DjangoPizzaria
    echo.
    netstat -an | findstr :8080 | findstr LISTENING
    if errorlevel 1 (
        echo.
        echo [AVISO] Porta 8080 nao esta escutando!
        echo Verifique os logs do servico.
    ) else (
        echo.
        echo [SUCESSO] Servidor rodando na porta 8080!
        echo.
        echo Testando conexao HTTP...
        curl -s http://localhost:8080 >nul 2>&1
        if errorlevel 1 (
            echo [!] Conexao HTTP falhou
        ) else (
            echo [OK] Servidor respondendo!
        )
    )
)

echo.
echo ============================================
echo Para ver logs em tempo real:
echo   type logs\service\servico.log
echo ============================================
echo.
pause