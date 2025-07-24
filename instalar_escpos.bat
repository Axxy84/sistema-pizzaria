@echo off
echo ============================================
echo   INSTALAR PYTHON-ESCPOS PARA IMPRESSAO
echo ============================================
echo.

echo [1] Ativando ambiente virtual...
call .venv\Scripts\activate.bat

echo.
echo [2] Instalando python-escpos...
pip install python-escpos

echo.
echo [3] Instalando pyusb para suporte USB...
pip install pyusb

echo.
echo [4] Instalando pyserial para portas seriais...
pip install pyserial

echo.
echo [5] Instalando Pillow para imagens (logo)...
pip install Pillow

echo.
echo ============================================
echo   INSTALACAO CONCLUIDA!
echo ============================================
echo.
echo Agora podemos usar comandos ESC/POS nativos!
echo.
pause