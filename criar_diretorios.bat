@echo off
echo Criando diretórios necessários...

:: Criar diretório static se não existir
if not exist "static" (
    mkdir static
    echo [✓] Diretório 'static' criado
) else (
    echo [✓] Diretório 'static' já existe
)

:: Criar subdiretórios do static
if not exist "static\css" mkdir static\css
if not exist "static\js" mkdir static\js
if not exist "static\images" mkdir static\images
if not exist "static\fonts" mkdir static\fonts

:: Criar outros diretórios
if not exist "media" mkdir media
if not exist "media\produtos" mkdir media\produtos
if not exist "staticfiles" mkdir staticfiles
if not exist "logs" mkdir logs
if not exist "backups" mkdir backups

echo [✓] Todos os diretórios criados com sucesso!