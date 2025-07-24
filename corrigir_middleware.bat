@echo off
REM Script para corrigir automaticamente o erro de middleware

echo ============================================
echo   CORRIGINDO ERRO DE MIDDLEWARE
echo ============================================
echo.

echo [1] Fazendo backup do settings.py...
copy DjangoProject\settings.py DjangoProject\settings_backup.py >nul

echo.
echo [2] Executando correção...
call .venv\Scripts\activate.bat
python fix_middleware.py

echo.
echo [3] Aplicando correção automaticamente...

REM Cria um script Python temporário para corrigir o settings.py
(
echo import re
echo 
echo # Lê o arquivo settings.py
echo with open('DjangoProject/settings.py', 'r', encoding='utf-8'^) as f:
echo     content = f.read(^)
echo 
echo # Define o novo MIDDLEWARE
echo new_middleware = """MIDDLEWARE = [
echo     'django.middleware.security.SecurityMiddleware',
echo     'whitenoise.middleware.WhiteNoiseMiddleware',
echo     'django.contrib.sessions.middleware.SessionMiddleware',
echo     'corsheaders.middleware.CorsMiddleware',
echo     'django.middleware.common.CommonMiddleware',
echo     'django.middleware.csrf.CsrfViewMiddleware',
echo     'django.contrib.auth.middleware.AuthenticationMiddleware',
echo     'apps.core.middleware.NoAuthMiddleware',  # Adiciona usuário falso
echo     'django.contrib.messages.middleware.MessageMiddleware',
echo     'django.middleware.clickjacking.XFrameOptionsMiddleware',
echo     'django.middleware.gzip.GZipMiddleware',
echo     'debug_toolbar.middleware.DebugToolbarMiddleware',
echo ]"""
echo 
echo # Substitui a seção MIDDLEWARE
echo pattern = r'MIDDLEWARE\s*=\s*\[[^\]]+\]'
echo content = re.sub(pattern, new_middleware, content, flags=re.DOTALL^)
echo 
echo # Salva o arquivo
echo with open('DjangoProject/settings.py', 'w', encoding='utf-8'^) as f:
echo     f.write(content^)
echo 
echo print("✅ Settings.py corrigido!"^)
) > fix_settings_temp.py

python fix_settings_temp.py
del fix_settings_temp.py

echo.
echo [4] Testando servidor...
echo.
echo Iniciando servidor (Ctrl+C para parar)...
echo ============================================
echo.

python run_no_auth.py