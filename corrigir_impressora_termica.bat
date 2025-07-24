@echo off
echo ============================================
echo   CORRIGIR IMPRESSORA TERMICA - CARACTERES ESTRANHOS
echo ============================================
echo.
echo PROBLEMA: Sai papel mas com interrogacoes/caracteres estranhos
echo CAUSA: Driver incorreto ou modo de impressao errado
echo.

echo [1] SOLUCAO 1: Mudar para driver GENERIC TEXT
echo ============================================
echo.
echo 1. Va em Configuracoes > Impressoras e scanners
echo 2. Clique na KNUP KP-IM609
echo 3. Clique em "Gerenciar" 
echo 4. Clique em "Propriedades da impressora"
echo 5. Aba "Avancado"
echo 6. Clique em "Novo Driver..."
echo 7. Escolha:
echo    Fabricante: Generic
echo    Impressora: Generic / Text Only
echo 8. Conclua a instalacao
echo.
pause

echo.
echo [2] SOLUCAO 2: Configurar modo RAW
echo ============================================
echo.
echo Nas propriedades da impressora:
echo 1. Aba "Avancado"
echo 2. Desmarque "Ativar recursos de impressao avancados"
echo 3. Processador de impressao: WinPrint
echo 4. Tipo de dados padrao: RAW
echo.
pause

echo.
echo [3] SOLUCAO 3: Driver ESC/POS
echo ============================================
echo.
echo Impressoras termicas usam comandos ESC/POS
echo Se nao tiver o driver Generic, procure por:
echo - ESC/POS
echo - POS Printer
echo - Thermal Printer
echo - Epson TM-T20 (compativel)
echo.
pause

echo.
echo [4] Criando impressora de teste...
echo ============================================
echo.

echo Adicionando porta para impressora generica...
cscript C:\Windows\System32\Printing_Admin_Scripts\pt-BR\prnport.vbs -a -r "KNUP_RAW" -h "127.0.0.1" -o raw -n 9100 2>nul

echo.
echo Para adicionar manualmente:
echo 1. Adicione uma nova impressora
echo 2. "A impressora que eu quero nao esta listada"
echo 3. "Adicionar uma impressora local"
echo 4. Use a porta USB existente da KNUP
echo 5. Fabricante: Generic
echo 6. Modelo: Generic / Text Only
echo 7. Nome: KNUP_GENERICA
echo.
pause