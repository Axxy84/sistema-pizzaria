@echo off
echo ============================================
echo   REINICIAR SPOOLER DE IMPRESSAO
echo ============================================
echo.
echo EXECUTE COMO ADMINISTRADOR!
echo.

echo [1] Parando spooler...
net stop spooler
echo.

echo [2] Limpando fila de impressao...
del /q /f "%SystemRoot%\System32\spool\PRINTERS\*.*" 2>nul
echo.

echo [3] Iniciando spooler...
net start spooler
echo.

echo [4] Verificando status...
sc query spooler | findstr STATE
echo.

echo ============================================
echo   SPOOLER REINICIADO!
echo ============================================
echo.
echo Tente imprimir novamente.
echo.
pause