@echo off
echo ============================================
echo   STATUS DO SERVIDOR DJANGO
echo ============================================
echo.

echo [1] Verificando servicos Windows...
echo ------------------------------------
sc query DjangoPizzariaAuto 2>nul | findstr "STATE"
if errorlevel 1 (
    echo Servico DjangoPizzariaAuto: NAO INSTALADO
) 

sc query DjangoPizzaria 2>nul | findstr "STATE"
if errorlevel 1 (
    echo Servico DjangoPizzaria: NAO INSTALADO
)

echo.
echo [2] Verificando processos Python...
echo ------------------------------------
tasklist | findstr python.exe
if errorlevel 1 (
    echo Nenhum processo Python rodando
)

echo.
echo [3] Verificando porta 8080...
echo ------------------------------------
netstat -an | findstr :8080 | findstr LISTENING
if errorlevel 1 (
    echo Porta 8080: LIVRE
) else (
    echo Porta 8080: EM USO (servidor rodando)
)

echo.
echo [4] Testando acesso HTTP...
echo ------------------------------------
curl -s -o nul -w "localhost:8080 - Status: %%{http_code}\n" http://localhost:8080 2>nul

echo.
echo ============================================
echo   OPCOES DISPONIVEIS:
echo ============================================
echo.
echo - Para INICIAR:    reiniciar_servidor.bat
echo - Para PARAR:      parar_servidor.bat
echo - Para REINSTALAR: inicializacao_automatica_completa.bat
echo.
pause