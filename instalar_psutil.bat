@echo off
echo ============================================
echo   INSTALAR PSUTIL PARA MONITORAMENTO
echo ============================================
echo.

echo [1] Ativando ambiente virtual...
call .venv\Scripts\activate.bat

echo.
echo [2] Instalando psutil...
pip install psutil

echo.
echo ============================================
echo   INSTALACAO CONCLUIDA!
echo ============================================
echo.
echo O indicador de status do servidor agora funcionara corretamente.
echo.
pause