@echo off
echo.
echo ========================================
echo   SISTEMA SEM AUTENTICACAO (DEV ONLY)
echo ========================================
echo.
echo ATENCAO: Isso e APENAS para desenvolvimento!
echo.
echo O sistema sera iniciado com:
echo - Acesso livre a todas as paginas
echo - Usuario temporario automatico
echo - Sem necessidade de login
echo.
set /p confirma="Digite SIM para continuar: "

if /i "%confirma%" neq "SIM" (
    echo.
    echo Operacao cancelada.
    pause
    exit
)

echo.
echo Iniciando servidor...
echo.

set DJANGO_SETTINGS_MODULE=settings_no_auth
python manage.py runserver

pause