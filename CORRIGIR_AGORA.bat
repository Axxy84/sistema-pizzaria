@echo off
echo ============================================
echo   CORRECAO RAPIDA DO ERRO
echo ============================================
echo.

echo [1] Fazendo backup...
copy DjangoProject\settings.py DjangoProject\settings_backup_%date:~-4,4%%date:~-10,2%%date:~-7,2%.py >nul

echo [2] Aplicando correcao...
python fix_settings_now.py

echo.
echo [3] Testando servidor...
echo.
python manage.py runserver 0.0.0.0:8080