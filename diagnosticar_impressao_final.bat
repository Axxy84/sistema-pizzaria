@echo off
echo ============================================
echo   DIAGNOSTICO FINAL DE IMPRESSAO
echo ============================================
echo.

echo [1] Verificando impressoras instaladas...
echo ============================================
wmic printer get name,drivername,portname,default
echo.

echo [2] Verificando impressora padrao...
echo ============================================
wmic printer where "default=TRUE" get name,portname,drivername
echo.

echo [3] Testando com diferentes metodos...
echo ============================================
echo.

echo METODO 1: Criando arquivo teste...
(
echo ========================================
echo         TESTE DIRETO 1
echo ========================================
echo Data/Hora: %date% %time%
echo.
echo Se voce consegue ler isso,
echo a impressora esta funcionando!
echo ========================================
echo.
echo.
echo.
) > teste_direto.txt

echo.
echo METODO 2: Enviando com PRINT...
print teste_direto.txt
echo.

echo METODO 3: Enviando com COPY para portas...
echo.
echo Testando USB001...
copy teste_direto.txt USB001 2>nul
echo.
echo Testando USB002...
copy teste_direto.txt USB002 2>nul
echo.
echo Testando LPT1...
copy teste_direto.txt LPT1 2>nul
echo.

echo METODO 4: Enviando com TYPE...
echo.
echo Procurando porta da KNUP...
for /f "tokens=2 delims==" %%a in ('wmic printer where "name like '%%KNUP%%'" get portname /value 2^>nul ^| findstr "="') do set PORTA_KNUP=%%a

if defined PORTA_KNUP (
    echo Porta encontrada: %PORTA_KNUP%
    echo Enviando...
    type teste_direto.txt > %PORTA_KNUP% 2>nul
) else (
    echo Porta KNUP nao encontrada
)

echo.
echo ============================================
echo   VERIFIQUE:
echo ============================================
echo.
echo 1. A impressora esta ligada?
echo 2. Tem papel?
echo 3. O cabo USB esta conectado?
echo 4. A impressora esta como PADRAO no Windows?
echo.
echo Se nada funcionou, tente:
echo - Reiniciar a impressora
echo - Reinstalar o driver como Generic/Text Only
echo - Usar o software da propria KNUP
echo.
pause