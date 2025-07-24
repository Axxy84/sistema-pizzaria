@echo off
chcp 65001 > nul
title Instalador de Serviço - Sistema Pizzaria

echo ========================================
echo   INSTALADOR DE SERVIÇO WINDOWS
echo ========================================
echo.
echo ATENÇÃO: Execute este arquivo como ADMINISTRADOR!
echo.

:: Verificar privilégios de administrador
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERRO] Este script precisa ser executado como Administrador!
    echo.
    echo Clique com botão direito e selecione "Executar como administrador"
    pause
    exit /b 1
)

:: Instalar pywin32 se necessário
echo Instalando dependências do serviço...
call .venv\Scripts\activate.bat
pip install pywin32
echo.

:: Instalar serviço
echo Instalando serviço...
python pizzaria_service.py install

:: Configurar serviço para iniciar automaticamente
echo.
echo Configurando serviço para iniciar automaticamente...
sc config PizzariaSystem start= auto

:: Iniciar serviço
echo.
echo Iniciando serviço...
python pizzaria_service.py start

echo.
echo ========================================
echo   SERVIÇO INSTALADO COM SUCESSO!
echo ========================================
echo.
echo O sistema agora está rodando como serviço do Windows.
echo.
echo Comandos úteis:
echo   - Parar serviço: net stop PizzariaSystem
echo   - Iniciar serviço: net start PizzariaSystem
echo   - Remover serviço: python pizzaria_service.py remove
echo.
echo Acesse o sistema em: http://localhost:8000
echo.
pause