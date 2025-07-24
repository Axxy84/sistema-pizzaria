@echo off
echo ============================================
echo   DIAGNOSTICO IMPRESSORA KNUP KP-IM609
echo ============================================
echo.

echo [1] Listando impressoras instaladas...
echo ----------------------------
wmic printer get name,drivername,portname,printerstatus,status
echo.

echo [2] Verificando spooler de impressao...
echo ----------------------------
sc query spooler
echo.

echo [3] Verificando fila de impressao...
echo ----------------------------
wmic printjob get name,status,totalpages,document
echo.

echo [4] Portas de impressora...
echo ----------------------------
wmic port get name,description
echo.

echo [5] Drivers instalados...
echo ----------------------------
wmic printerdriver get name,version,driverpath | findstr /i "knup\|kp-im\|609"
echo.

echo [6] Status detalhado da Knup...
echo ----------------------------
wmic printer where "name like '%%KNUP%%' or name like '%%KP-IM%%' or name like '%%609%%'" get name,status,printerstatus,drivername,portname,default /format:list
echo.

echo [7] Verificando servicos relacionados...
echo ----------------------------
echo Spooler:
sc query spooler | findstr STATE
echo.
echo Print Notifications:
sc query PrintNotify | findstr STATE 2>nul
echo.

echo [8] Logs de eventos recentes...
echo ----------------------------
wevtutil qe System /c:10 /f:text /q:"*[System[(EventID=7000 or EventID=7001 or EventID=7002) and Provider[@Name='Service Control Manager']]]" 2>nul | findstr /i "print\|spool"
echo.

echo ============================================
echo   SOLUCOES COMUNS:
echo ============================================
echo.
echo 1. Execute: reiniciar_spooler.bat
echo 2. Verifique se a porta esta correta (USB/LPT)
echo 3. Teste com pagina de teste do Windows
echo 4. Verifique cabo USB/conexao
echo.
pause