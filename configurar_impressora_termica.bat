@echo off
echo ============================================
echo   CONFIGURAR IMPRESSORA TERMICA KNUP KP-IM609
echo ============================================
echo.

echo [1] Definindo impressora padrao...
echo ----------------------------
wmic printer where "name like '%%KNUP%%' or name like '%%KP-IM%%' or name like '%%609%%'" call setdefaultprinter
echo.

echo [2] Configurando porta...
echo ----------------------------
echo Impressoras termicas geralmente usam:
echo - USB001, USB002, etc (para USB)
echo - COM1, COM2, etc (para serial)
echo - LPT1 (para paralela)
echo.

echo [3] Testando impressao direta...
echo ----------------------------
echo Enviando comando de teste...
(
echo .
echo TESTE DE IMPRESSAO
echo KNUP KP-IM609
echo .
echo %date% %time%
echo .
echo ================================
echo .
) > teste_impressao.txt

echo.
echo [4] Opcoes de teste:
echo ----------------------------
echo.
echo A) Teste via Windows:
echo    - Va em Configuracoes > Impressoras
echo    - Clique com botao direito na KNUP
echo    - Escolha "Propriedades da impressora"
echo    - Clique em "Imprimir pagina de teste"
echo.
echo B) Teste via comando:
echo    - Execute: notepad teste_impressao.txt
echo    - Pressione Ctrl+P e imprima
echo.
echo C) Para impressora termica de cupom:
echo    - Verifique tamanho do papel (58mm ou 80mm)
echo    - Configure nas propriedades da impressora
echo.

echo [5] Drivers alternativos...
echo ----------------------------
echo Se nao funcionar, tente driver generico:
echo - "Generic / Text Only"
echo - "Generic ESC/POS"
echo.

pause