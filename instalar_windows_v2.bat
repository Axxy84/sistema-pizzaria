@echo off
chcp 65001 > nul
title Instalador - Sistema Pizzaria v2.0
color 0A

echo.
echo ╔════════════════════════════════════════════╗
echo ║     INSTALADOR DO SISTEMA PIZZARIA v2.0    ║
echo ╠════════════════════════════════════════════╣
echo ║  Desenvolvido por: Sua Empresa             ║
echo ║  Suporte: (XX) XXXXX-XXXX                  ║
echo ╚════════════════════════════════════════════╝
echo.

:: Verificar execução como administrador
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo [AVISO] Execute este instalador como Administrador!
    echo Clique com botão direito e selecione "Executar como administrador"
    pause
    exit /b 1
)

:: Verificar se Python está instalado
echo [1/8] Verificando Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo ╔════════════════════════════════════════════╗
    echo ║              PYTHON NÃO ENCONTRADO         ║
    echo ╠════════════════════════════════════════════╣
    echo ║  1. Baixe Python em:                       ║
    echo ║     https://www.python.org/downloads/      ║
    echo ║                                            ║
    echo ║  2. Durante a instalação, marque:         ║
    echo ║     [✓] Add Python to PATH                ║
    echo ║                                            ║
    echo ║  3. Reinicie o computador                  ║
    echo ║  4. Execute este instalador novamente      ║
    echo ╚════════════════════════════════════════════╝
    echo.
    pause
    exit /b 1
)

python --version
echo [✓] Python encontrado
echo.

:: Criar ambiente virtual se não existir
echo [2/8] Configurando ambiente virtual...
if not exist ".venv" (
    python -m venv .venv
    if %errorlevel% neq 0 (
        echo [ERRO] Falha ao criar ambiente virtual
        pause
        exit /b 1
    )
    echo [✓] Ambiente virtual criado
) else (
    echo [✓] Ambiente virtual já existe
)

:: Ativar ambiente virtual
call .venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo [ERRO] Falha ao ativar ambiente virtual
    pause
    exit /b 1
)

:: Atualizar pip
echo.
echo [3/8] Atualizando pip...
python -m pip install --upgrade pip --quiet
echo [✓] Pip atualizado

:: Instalar dependências
echo.
echo [4/8] Instalando dependências (pode demorar alguns minutos)...
pip install -r requirements.txt --quiet --disable-pip-version-check
if %errorlevel% neq 0 (
    echo [ERRO] Falha ao instalar dependências
    echo Verifique sua conexão com a internet
    pause
    exit /b 1
)
echo [✓] Dependências instaladas

:: Criar diretórios necessários
echo.
echo [5/8] Criando estrutura de diretórios...
if not exist "media" mkdir media
if not exist "media\produtos" mkdir media\produtos
if not exist "staticfiles" mkdir staticfiles
if not exist "logs" mkdir logs
if not exist "backups" mkdir backups
echo [✓] Diretórios criados

:: Criar arquivo .env se não existir
echo.
echo [6/8] Configurando variáveis de ambiente...
if not exist ".env" (
    (
        echo # Configurações do Sistema Pizzaria
        echo DEBUG=True
        echo SECRET_KEY=sua-chave-secreta-aqui-mude-em-producao
        echo ALLOWED_HOSTS=localhost,127.0.0.1
        echo.
        echo # Banco de dados Supabase
        echo DATABASE_HOST=aws-0-sa-east-1.pooler.supabase.com
        echo DATABASE_PORT=5432
        echo DATABASE_NAME=postgres
        echo DATABASE_USER=postgres.aewcurtmikqelqykpqoa
        echo DATABASE_PASSWORD=sua_senha_aqui
        echo # DATABASE_URL=postgresql://user:pass@host:port/dbname
        echo.
        echo # Redis Cache (opcional)
        echo REDIS_URL=redis://localhost:6379/0
    ) > .env
    echo [✓] Arquivo .env criado (configure se necessário)
) else (
    echo [✓] Arquivo .env já existe
)

:: Executar migrações
echo.
echo [7/8] Configurando banco de dados...
python manage.py migrate --run-syncdb --noinput --settings=settings_fast
if %errorlevel% neq 0 (
    echo [ERRO] Falha ao aplicar migrações
    echo Tentando com configurações padrão...
    python manage.py migrate --run-syncdb --noinput
    if %errorlevel% neq 0 (
        echo [ERRO] Falha persistente nas migrações
        pause
        exit /b 1
    )
)
echo [✓] Banco de dados configurado

:: Coletar arquivos estáticos
echo.
echo [8/8] Preparando arquivos estáticos...
python manage.py collectstatic --noinput --clear --settings=settings_fast >nul 2>&1
if %errorlevel% neq 0 (
    python manage.py collectstatic --noinput --clear >nul 2>&1
)
echo [✓] Arquivos estáticos preparados

:: Criar usuário admin
echo.
echo ╔════════════════════════════════════════════╗
echo ║         CRIAR USUÁRIO ADMINISTRADOR        ║
echo ╚════════════════════════════════════════════╝
echo.
echo Deseja criar um usuário administrador agora? (S/N)
set /p criar_admin=Resposta: 
if /i "%criar_admin%"=="S" (
    echo.
    python manage.py createsuperuser --settings=settings_fast
    if %errorlevel% neq 0 (
        python manage.py createsuperuser
    )
)

:: Carregar dados iniciais
echo.
echo Deseja carregar dados de exemplo? (S/N)
set /p carregar_dados=Resposta: 
if /i "%carregar_dados%"=="S" (
    echo Carregando dados...
    python setup_initial_data.py
    echo [✓] Dados carregados
)

:: Criar atalhos
echo.
echo Deseja criar atalhos na área de trabalho? (S/N)
set /p criar_atalhos=Resposta: 
if /i "%criar_atalhos%"=="S" (
    call criar_atalhos.bat
)

:: Finalização
cls
echo.
echo ╔════════════════════════════════════════════╗
echo ║      INSTALAÇÃO CONCLUÍDA COM SUCESSO!     ║
echo ╠════════════════════════════════════════════╣
echo ║                                            ║
echo ║  Para iniciar o sistema:                   ║
echo ║  → Execute: iniciar_pizzaria.bat           ║
echo ║                                            ║
echo ║  Acesso ao sistema:                        ║
echo ║  → http://localhost:8000                   ║
echo ║  → Admin: http://localhost:8000/admin      ║
echo ║                                            ║
echo ║  Documentação:                             ║
echo ║  → Leia INSTALACAO_CLIENTE.md              ║
echo ║                                            ║
echo ╚════════════════════════════════════════════╝
echo.
echo Pressione qualquer tecla para finalizar...
pause >nul