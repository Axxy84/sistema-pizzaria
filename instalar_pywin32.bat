@echo off
echo ============================================
echo   INSTALAR PYWIN32 PARA IMPRESSAO
echo ============================================
echo.

echo [1] Ativando ambiente virtual...
call .venv\Scripts\activate.bat

echo.
echo [2] Instalando pywin32...
pip install pywin32

echo.
echo [3] Finalizando instalacao...
python .venv\Scripts\pywin32_postinstall.py -install 2>nul

echo.
echo ============================================
echo   INSTALACAO CONCLUIDA!
echo ============================================
echo.
echo Agora execute: python testar_impressao_direta.py
echo.
pause