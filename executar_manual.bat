@echo off
REM Script para executar o servidor manualmente (debug)

echo ============================================
echo   EXECUCAO MANUAL DO SERVIDOR
echo ============================================
echo.

REM Para qualquer serviço rodando
echo [1] Parando servico (se estiver rodando)...
net stop DjangoPizzaria >nul 2>&1

REM Mata processos na porta
echo [2] Liberando porta 8080...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8080') do (
    taskkill /F /PID %%a >nul 2>&1
)

REM Ativa ambiente
echo [3] Ativando ambiente virtual...
call .venv\Scripts\activate.bat

echo.
echo [4] Informacoes do ambiente:
echo Python: 
python --version
echo.
echo Pip packages:
pip list | findstr Django
echo.

REM Verifica arquivo
echo [5] Verificando arquivo run_no_auth.py...
if not exist "run_no_auth.py" (
    echo [ERRO] Arquivo run_no_auth.py NAO ENCONTRADO!
    echo.
    echo Criando arquivo run_no_auth.py basico...
    (
        echo import os
        echo import sys
        echo.
        echo # Adiciona o diretorio do projeto ao path
        echo sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))^)
        echo.
        echo # Configura o Django
        echo os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoProject.settings'^)
        echo.
        echo # Importa e executa o Django
        echo import django
        echo django.setup(^)
        echo.
        echo # Executa o servidor
        echo from django.core.management import execute_from_command_line
        echo execute_from_command_line(['manage.py', 'runserver', '0.0.0.0:8080']^)
    ) > run_no_auth.py
    echo.
    echo Arquivo criado! Tentando executar...
)

echo.
echo [6] Executando servidor (Ctrl+C para parar)...
echo ============================================
echo.

python run_no_auth.py