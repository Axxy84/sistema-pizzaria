@echo off
REM Wrapper para executar Django no contexto do serviço Windows

echo [%date% %time%] Iniciando wrapper do servico... >> logs\service\wrapper.log

REM Muda para o diretório correto
cd /d "C:\Users\User\Documents\sistema-pizzaria-master"

REM Define variáveis de ambiente
set PYTHONUNBUFFERED=1
set DJANGO_SETTINGS_MODULE=DjangoProject.settings

REM Ativa o ambiente virtual
echo [%date% %time%] Ativando ambiente virtual... >> logs\service\wrapper.log
call .venv\Scripts\activate.bat

REM Verifica Python
python --version >> logs\service\wrapper.log 2>&1

REM Executa o servidor
echo [%date% %time%] Iniciando servidor Django... >> logs\service\wrapper.log
python run_no_auth.py