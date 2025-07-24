@echo off
REM Script para diagnosticar problemas com o serviço Django

echo ============================================
echo   DIAGNOSTICO DO SERVICO DJANGO
echo ============================================
echo.

REM Verifica status do serviço
echo [1] Status do Servico:
echo --------------------------------------------
sc query DjangoPizzaria
echo.

REM Verifica se a porta está escutando
echo [2] Verificando porta 8080:
echo --------------------------------------------
netstat -an | findstr :8080
echo.

REM Verifica processos Python
echo [3] Processos Python rodando:
echo --------------------------------------------
tasklist | findstr python
echo.

REM Verifica logs
echo [4] Ultimas linhas do log de servico:
echo --------------------------------------------
if exist "logs\service\servico.log" (
    echo === SERVICO.LOG ===
    type "logs\service\servico.log" | more +eof-20
) else (
    echo Arquivo servico.log nao encontrado
)
echo.

if exist "logs\service\erro.log" (
    echo === ERRO.LOG ===
    type "logs\service\erro.log" | more +eof-20
) else (
    echo Arquivo erro.log nao encontrado
)
echo.

REM Testa executar diretamente
echo [5] Testando execucao direta:
echo --------------------------------------------
echo Tentando executar o servidor diretamente...
echo.

REM Para o serviço temporariamente
net stop DjangoPizzaria >nul 2>&1

REM Ativa ambiente virtual e testa
call .venv\Scripts\activate.bat
python --version
echo.

REM Verifica se o script existe
if exist "run_no_auth.py" (
    echo Arquivo run_no_auth.py encontrado!
    echo.
    echo Tentando executar (Ctrl+C para parar):
    echo --------------------------------------------
    python run_no_auth.py
) else (
    echo [ERRO] Arquivo run_no_auth.py NAO encontrado!
    echo.
    echo Arquivos .py na pasta:
    dir *.py
)

pause