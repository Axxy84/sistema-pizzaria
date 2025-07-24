@echo off
echo ============================================
echo   CONFIGURAR IMPRESSAO KNUP - USB001/USB002
echo ============================================
echo.

echo [1] Testando qual porta USB funciona...
echo.

echo Criando arquivo de teste...
(
echo ========================================
echo         TESTE PORTA USB
echo ========================================
echo.
echo Se este texto aparecer na impressora,
echo a configuracao esta correta!
echo.
echo Data: %date% %time%
echo.
echo ========================================
echo.
echo.
echo.
) > teste_usb.txt

echo.
echo Testando USB001...
copy teste_usb.txt USB001 >nul 2>&1
if %errorlevel% == 0 (
    echo [OK] USB001 funcionou!
    set PORTA_CORRETA=USB001
) else (
    echo [X] USB001 falhou
)

echo.
echo Testando USB002...
copy teste_usb.txt USB002 >nul 2>&1
if %errorlevel% == 0 (
    echo [OK] USB002 funcionou!
    set PORTA_CORRETA=USB002
) else (
    echo [X] USB002 falhou
)

echo.
echo ============================================
echo   RESULTADO:
echo ============================================
echo.

if defined PORTA_CORRETA (
    echo SUCESSO! Sua impressora esta na porta: %PORTA_CORRETA%
    echo.
    echo Salvando configuracao...
    echo %PORTA_CORRETA% > knup_porta.txt
    echo.
    echo A impressora KNUP esta configurada!
) else (
    echo ERRO: Nenhuma porta USB funcionou
    echo Verifique se a impressora esta ligada e conectada
)

echo.
pause

del teste_usb.txt 2>nul