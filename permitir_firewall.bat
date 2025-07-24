@echo off
echo ============================================
echo   ADICIONAR REGRA NO FIREWALL WINDOWS
echo ============================================
echo.
echo ESTE SCRIPT DEVE SER EXECUTADO COMO ADMINISTRADOR!
echo.

echo [1] Removendo regras antigas...
netsh advfirewall firewall delete rule name="Django Dev Server 8080" >nul 2>&1
netsh advfirewall firewall delete rule name="Python Django" >nul 2>&1

echo.
echo [2] Adicionando novas regras...
echo.

echo Regra 1: Porta 8080 TCP entrada
netsh advfirewall firewall add rule name="Django Dev Server 8080" dir=in action=allow protocol=TCP localport=8080

echo.
echo Regra 2: Porta 8080 TCP saida
netsh advfirewall firewall add rule name="Django Dev Server 8080 Out" dir=out action=allow protocol=TCP localport=8080

echo.
echo Regra 3: Python.exe no venv
netsh advfirewall firewall add rule name="Python Django" dir=in action=allow program="%CD%\.venv\Scripts\python.exe" enable=yes

echo.
echo [3] Verificando regras criadas...
netsh advfirewall firewall show rule name="Django Dev Server 8080"

echo.
echo ============================================
echo   REGRAS ADICIONADAS COM SUCESSO!
echo ============================================
echo.
echo Agora tente acessar:
echo - http://localhost:8080
echo - http://127.0.0.1:8080
echo.
pause