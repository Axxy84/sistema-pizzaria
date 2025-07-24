@echo off
echo ============================================
echo   CORRIGINDO RUN_NO_AUTH.PY
echo ============================================
echo.

echo [1] Criando backup...
copy run_no_auth.py run_no_auth_backup.py >nul

echo [2] Criando novo run_no_auth.py...
(
echo #!/usr/bin/env python
echo """
echo Script para executar o sistema diretamente
echo """
echo.
echo import os
echo import sys
echo import subprocess
echo.
echo # Banner de aviso
echo print("\n" + "="*60)
echo print("\n  INICIANDO SERVIDOR DJANGO")
echo print("\n" + "="*60 + "\n")
echo.
echo print("Servidor sera iniciado em: http://localhost:8080")
echo print("\nPara parar: CTRL+C")
echo print("\n" + "-"*60 + "\n")
echo.
echo # Executar o servidor
echo try:
echo     subprocess.run([sys.executable, 'manage.py', 'runserver', '0.0.0.0:8080'])
echo except KeyboardInterrupt:
echo     print("\n\nServidor parado.")
) > run_no_auth_fixed.py

echo.
echo [3] Testando servidor corrigido...
echo.
python run_no_auth_fixed.py