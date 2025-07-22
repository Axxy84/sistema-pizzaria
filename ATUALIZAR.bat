@echo off
echo ATUALIZANDO SISTEMA...
git fetch origin
git reset --hard origin/master
echo.
echo SISTEMA ATUALIZADO!
pause