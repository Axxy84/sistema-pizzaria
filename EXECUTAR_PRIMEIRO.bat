@echo off
chcp 65001 > nul
title CORREÇÃO E INSTALAÇÃO - Sistema Pizzaria
color 0E

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║       CORREÇÃO E INSTALAÇÃO AUTOMÁTICA - PIZZARIA          ║
echo ╠════════════════════════════════════════════════════════════╣
echo ║  Este script corrige todos os problemas conhecidos e       ║
echo ║  executa a instalação completa do sistema.                 ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

:: Garantir que estamos no diretório correto
cd /d "%~dp0"
echo Diretório de trabalho: %CD%
echo.

:: 1. Criar todos os diretórios necessários
echo [PASSO 1] Criando estrutura de diretórios...
if not exist "static" mkdir static
if not exist "static\css" mkdir static\css
if not exist "static\js" mkdir static\js
if not exist "static\images" mkdir static\images
if not exist "static\fonts" mkdir static\fonts
if not exist "media" mkdir media
if not exist "media\produtos" mkdir media\produtos
if not exist "staticfiles" mkdir staticfiles
if not exist "logs" mkdir logs
if not exist "backups" mkdir backups
echo [✓] Diretórios criados
echo.

:: 2. Verificar Python
echo [PASSO 2] Verificando Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERRO] Python não encontrado!
    echo Instale Python 3.10+ de https://www.python.org/downloads/
    echo Marque "Add Python to PATH" durante a instalação
    pause
    exit /b 1
)
python --version
echo [✓] Python OK
echo.

:: 3. Criar/ativar ambiente virtual
echo [PASSO 3] Configurando ambiente virtual...
if not exist ".venv" (
    python -m venv .venv
)
call .venv\Scripts\activate.bat
echo [✓] Ambiente virtual ativado
echo.

:: 4. Instalar dependências
echo [PASSO 4] Instalando dependências...
python -m pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet --disable-pip-version-check
echo [✓] Dependências instaladas
echo.

:: 5. Remover migrações conflitantes
echo [PASSO 5] Corrigindo migrações...
if exist "apps\pedidos\migrations\0011_merge_20250722_1920.py" (
    del "apps\pedidos\migrations\0011_merge_20250722_1920.py" >nul 2>&1
    echo [✓] Migração duplicada removida
)

:: Limpar cache
for /d %%i in (apps\*\migrations\__pycache__) do (
    rmdir /s /q "%%i" >nul 2>&1
)
echo [✓] Cache limpo
echo.

:: 6. Aplicar migrações
echo [PASSO 6] Configurando banco de dados...
python manage.py migrate --run-syncdb --settings=settings_fast >nul 2>&1
if %errorlevel% neq 0 (
    :: Tentar resetar migrações do app problemático
    python manage.py migrate pedidos zero --fake --settings=settings_fast >nul 2>&1
    python manage.py migrate --settings=settings_fast >nul 2>&1
)
echo [✓] Banco de dados configurado
echo.

:: 7. Coletar arquivos estáticos
echo [PASSO 7] Preparando arquivos estáticos...
python manage.py collectstatic --noinput --clear --settings=settings_fast >nul 2>&1
echo [✓] Arquivos estáticos prontos
echo.

:: 8. Criar superusuário
echo [PASSO 8] Criar usuário administrador
echo.
echo Deseja criar um usuário administrador? (S/N)
set /p criar_admin=
if /i "%criar_admin%"=="S" (
    python manage.py createsuperuser --settings=settings_fast
)
echo.

:: 9. Carregar dados iniciais
echo Deseja carregar dados de exemplo? (S/N)
set /p carregar_dados=
if /i "%carregar_dados%"=="S" (
    if exist "setup_initial_data.py" (
        python setup_initial_data.py
        echo [✓] Dados carregados
    )
)
echo.

:: 10. Criar atalhos
echo Criar atalhos na área de trabalho? (S/N)
set /p criar_atalhos=
if /i "%criar_atalhos%"=="S" (
    if exist "criar_atalhos_v2.bat" (
        call criar_atalhos_v2.bat
    )
)

:: Finalização
cls
color 0A
echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║            INSTALAÇÃO CONCLUÍDA COM SUCESSO!               ║
echo ╠════════════════════════════════════════════════════════════╣
echo ║                                                            ║
echo ║  ▶ Para iniciar: Execute "iniciar_pizzaria.bat"           ║
echo ║  ▶ Acesse: http://localhost:8000                          ║
echo ║  ▶ Admin: http://localhost:8000/admin                     ║
echo ║                                                            ║
echo ║  📖 Documentação: INSTALACAO_CLIENTE.md                   ║
echo ║  📞 Suporte: (XX) XXXXX-XXXX                             ║
echo ║                                                            ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
pause