@echo off
echo ========================================
echo     ENVIANDO MUDANCAS PARA GITHUB
echo ========================================
echo.

echo Verificando status...
git status

echo.
set /p mensagem="Digite a mensagem do commit: "

echo.
echo Adicionando arquivos...
git add .

echo.
echo Criando commit...
git commit -m "%mensagem%"

echo.
echo Enviando para GitHub...
git push origin master

if errorlevel 1 (
    echo.
    echo Tentando com main...
    git push origin main
)

echo.
echo ========================================
echo     MUDANCAS ENVIADAS!
echo ========================================
pause