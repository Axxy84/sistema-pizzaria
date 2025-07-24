@echo off
echo ========================================
echo     ATUALIZANDO SISTEMA PIZZARIA
echo ========================================
echo.

echo Baixando atualizacoes...
git pull origin master

echo.
echo Ativando ambiente virtual...
call .venv\Scripts\activate

echo.
echo Instalando dependencias...
pip install -r requirements.txt

echo.
echo Aplicando migracoes...
python manage.py migrate

echo.
echo ========================================
echo     ATUALIZACAO CONCLUIDA!
echo ========================================
echo.
echo Para iniciar o sistema, execute:
echo python manage.py runserver
echo.
pause