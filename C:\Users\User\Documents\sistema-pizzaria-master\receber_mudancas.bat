@echo off
echo ========================================
echo     RECEBENDO ATUALIZACOES DO GITHUB
echo ========================================
echo.

echo Baixando mudancas...
git pull origin master

if errorlevel 1 (
    echo.
    echo Tentando com main...
    git pull origin main
)

echo.
echo Instalando dependencias novas...
.venv\Scripts\activate && pip install -r requirements.txt

echo.
echo Aplicando migracoes...
.venv\Scripts\activate && python manage.py migrate

echo.
echo ========================================
echo     SISTEMA ATUALIZADO!
echo ========================================
pause