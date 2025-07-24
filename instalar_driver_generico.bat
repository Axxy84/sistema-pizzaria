@echo off
echo ============================================
echo   INSTALAR DRIVER GENERICO PARA TERMICA
echo ============================================
echo.
echo IMPORTANTE: Este processo resolve 90% dos problemas
echo de caracteres estranhos em impressoras termicas!
echo.

echo [OPCAO 1] INSTALACAO AUTOMATICA
echo ================================
echo.

echo Tentando adicionar driver Generic/Text Only...
rundll32 printui.dll,PrintUIEntry /ia /m "Generic / Text Only" /h "Intel" /v "Type 3 - User Mode" /f %windir%\inf\ntprint.inf

echo.
echo [OPCAO 2] INSTALACAO MANUAL (RECOMENDADO)
echo =========================================
echo.
echo 1. Pressione Windows + R
echo 2. Digite: control printers
echo 3. Clique em "Adicionar uma impressora"
echo 4. Clique em "A impressora que eu quero nao esta listada"
echo 5. Selecione "Adicionar uma impressora local..."
echo 6. IMPORTANTE: Use a porta existente da KNUP (USB00X)
echo 7. Na lista de fabricantes, escolha: Generic
echo 8. Na lista de impressoras, escolha: Generic / Text Only
echo 9. Use o driver existente
echo 10. Nome: KNUP_TEXTO (ou outro nome)
echo 11. NAO definir como padrao ainda
echo 12. Imprimir pagina de teste
echo.
pause

echo.
echo [TESTE RAPIDO]
echo ==============
echo.
echo Criando arquivo de teste simples...
(
echo ==============================
echo    TESTE DRIVER GENERICO
echo ==============================
echo.
echo Se voce consegue ler isto,
echo o driver generico funciona!
echo.
echo Data: %date%
echo Hora: %time%
echo.
echo ==============================
echo.
echo.
echo.
) > teste_generico.txt

echo.
echo Arquivo criado: teste_generico.txt
echo.
echo AGORA:
echo 1. Abra este arquivo no Notepad
echo 2. Imprima na impressora com driver generico
echo 3. Se funcionar, configure o sistema para usar essa impressora
echo.
notepad teste_generico.txt

pause