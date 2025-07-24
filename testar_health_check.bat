@echo off
echo ============================================
echo   TESTANDO HEALTH CHECK API
echo ============================================
echo.

echo [1] Testando endpoint /api/health/...
curl -s http://localhost:8080/api/health/ | python -m json.tool

echo.
echo [2] Testando com PowerShell...
powershell -Command "Invoke-WebRequest -Uri 'http://localhost:8080/api/health/' -UseBasicParsing | Select-Object -ExpandProperty Content | ConvertFrom-Json | ConvertTo-Json -Depth 10"

echo.
echo ============================================
echo.
echo Se aparecer JSON com status "healthy", esta funcionando!
echo Se der erro 404, precisamos reiniciar o servidor.
echo.
pause