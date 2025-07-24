@echo off
echo ============================================
echo   DIAGNOSTICO COMPLETO DO SERVIDOR
echo ============================================
echo.

echo [1] Informacoes do Sistema
echo ----------------------------
echo Usuario: %USERNAME%
echo Diretorio: %CD%
echo.

echo [2] Verificando Python
echo ----------------------------
where python
python --version
echo.

echo [3] Verificando Django
echo ----------------------------
python -c "import django; print(f'Django {django.get_version()}')"
echo.

echo [4] Verificando Variaveis de Ambiente
echo ----------------------------
echo DJANGO_SETTINGS_MODULE = %DJANGO_SETTINGS_MODULE%
echo PYTHONPATH = %PYTHONPATH%
echo.

echo [5] Testando importacao do settings
echo ----------------------------
python -c "from DjangoProject import settings; print('Settings OK')" 2>&1
echo.

echo [6] Verificando ALLOWED_HOSTS
echo ----------------------------
python -c "from DjangoProject.settings import ALLOWED_HOSTS; print(f'ALLOWED_HOSTS = {ALLOWED_HOSTS}')" 2>&1
echo.

echo [7] Verificando Firewall Windows
echo ----------------------------
netsh advfirewall show currentprofile | findstr "State"
echo.

echo [8] Regras de Firewall para Python
echo ----------------------------
netsh advfirewall firewall show rule name=all | findstr /i "python" | findstr /i "8080\|8000"
echo.

echo [9] Testando localhost vs 0.0.0.0
echo ----------------------------
echo.
echo Teste 1: localhost:8080
curl -I http://localhost:8080 2>&1 | findstr /i "HTTP\|refused\|timeout"
echo.
echo Teste 2: 127.0.0.1:8080
curl -I http://127.0.0.1:8080 2>&1 | findstr /i "HTTP\|refused\|timeout"
echo.
echo Teste 3: 0.0.0.0:8080 (invalido para cliente)
echo [Info] 0.0.0.0 e endereco de bind, nao de acesso
echo.

echo [10] Portas em uso
echo ----------------------------
netstat -an | findstr "LISTENING" | findstr ":80"
echo.

echo [11] Processos Python rodando
echo ----------------------------
tasklist | findstr python
echo.

echo [12] Testando DNS local
echo ----------------------------
nslookup localhost
ping -n 1 localhost | findstr /i "bytes\|unreachable"
echo.

echo [13] Arquivo hosts
echo ----------------------------
type C:\Windows\System32\drivers\etc\hosts | findstr -v "^#" | findstr "."
echo.

echo ============================================
echo   INICIANDO SERVIDOR DE TESTE
echo ============================================
echo.
echo O servidor sera iniciado em modo DEBUG
echo Observe as mensagens de erro
echo.
echo Pressione Ctrl+C quando terminar o teste
echo.
pause

call .venv\Scripts\activate.bat
set DJANGO_DEBUG=True
python manage.py runserver --verbosity 3 127.0.0.1:8080