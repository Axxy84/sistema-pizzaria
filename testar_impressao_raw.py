#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Teste de impressão RAW para impressora térmica
Corrige problema de caracteres estranhos/interrogações
"""
import os
import sys
import subprocess

def encontrar_impressora_knup():
    """Encontra o nome exato da impressora KNUP"""
    try:
        result = subprocess.run(['wmic', 'printer', 'get', 'name'], 
                              capture_output=True, text=True)
        for linha in result.stdout.split('\n'):
            if 'knup' in linha.lower() or 'kp-im' in linha.lower() or '609' in linha.lower():
                return linha.strip()
    except:
        pass
    return None

def criar_arquivo_teste():
    """Cria arquivo de teste em formato texto puro"""
    conteudo = """================================
    TESTE IMPRESSORA TERMICA    
       KNUP KP-IM609          
================================

PEDIDO: #0001
DATA: TESTE

--------------------------------
ITEM              QTD    VALOR
--------------------------------
Pizza Grande       1     45.00
Coca-Cola 2L       1      8.00
--------------------------------
TOTAL:                   53.00
--------------------------------

   OBRIGADO PELA PREFERENCIA!   

================================




"""
    
    # Salvar em diferentes codificações
    with open('teste_ascii.txt', 'w', encoding='ascii', errors='ignore') as f:
        f.write(conteudo)
    
    with open('teste_utf8.txt', 'w', encoding='utf-8') as f:
        f.write(conteudo)
    
    with open('teste_ansi.txt', 'w', encoding='cp1252') as f:
        f.write(conteudo)
    
    # Criar arquivo com comandos ESC/POS básicos
    with open('teste_escpos.txt', 'wb') as f:
        # Inicializar
        f.write(b'\x1B\x40')  # ESC @ - Inicializar impressora
        
        # Texto normal
        f.write(b'\x1B\x61\x01')  # ESC a 1 - Centralizar
        f.write(b'TESTE IMPRESSORA\n')
        f.write(b'KNUP KP-IM609\n')
        f.write(b'\x1B\x61\x00')  # ESC a 0 - Alinhar esquerda
        f.write(b'-' * 32 + b'\n')
        f.write(b'Pizza Grande     1    45.00\n')
        f.write(b'Refrigerante     2     6.00\n')
        f.write(b'-' * 32 + b'\n')
        f.write(b'TOTAL:               51.00\n')
        f.write(b'\n\n\n')
        
        # Cortar papel (se suportado)
        f.write(b'\x1D\x56\x00')  # GS V 0 - Corte total

def testar_impressao_metodo1(printer_name):
    """Método 1: Usando print direto do Windows"""
    print("\n[MÉTODO 1] Testando com comando PRINT...")
    
    arquivos = ['teste_ascii.txt', 'teste_ansi.txt', 'teste_utf8.txt']
    
    for arquivo in arquivos:
        if os.path.exists(arquivo):
            print(f"  Testando {arquivo}...")
            cmd = f'print /D:"{printer_name}" {arquivo}'
            os.system(cmd)
            input("  Pressione ENTER após verificar a impressão...")

def testar_impressao_metodo2(printer_name):
    """Método 2: Usando copy para porta"""
    print("\n[MÉTODO 2] Testando cópia direta...")
    
    # Encontrar porta da impressora
    result = subprocess.run(['wmic', 'printer', 'where', f'name="{printer_name}"', 
                           'get', 'portname'], capture_output=True, text=True)
    porta = None
    for linha in result.stdout.split('\n'):
        if 'USB' in linha or 'LPT' in linha:
            porta = linha.strip()
            break
    
    if porta:
        print(f"  Porta encontrada: {porta}")
        print(f"  Copiando para {porta}...")
        os.system(f'copy teste_ascii.txt {porta} 2>nul')
        input("  Pressione ENTER após verificar...")
    else:
        print("  Porta não encontrada")

def testar_impressao_metodo3(printer_name):
    """Método 3: Notepad com configuração"""
    print("\n[MÉTODO 3] Instruções para teste manual...")
    print("""
  1. Abra o arquivo teste_ascii.txt no Notepad
  2. Pressione Ctrl+P para imprimir
  3. Selecione a impressora KNUP
  4. Clique em "Preferências"
  5. Procure por opções como:
     - Modo: Texto/Text/RAW
     - Emulação: Nenhuma/None
     - Fonte: Usar fonte da impressora
  6. Imprima
  
  Pressione ENTER para abrir o Notepad...""")
    input()
    os.system('notepad teste_ascii.txt')

def main():
    print("="*50)
    print("   CORRIGIR IMPRESSÃO - CARACTERES ESTRANHOS")
    print("="*50)
    
    # Encontrar impressora
    printer_name = encontrar_impressora_knup()
    
    if not printer_name:
        printer_name = input("\nDigite o nome exato da impressora KNUP: ")
    else:
        print(f"\nImpressora encontrada: {printer_name}")
    
    # Criar arquivos de teste
    print("\nCriando arquivos de teste...")
    criar_arquivo_teste()
    
    # Menu de testes
    while True:
        print("\n" + "="*50)
        print("ESCOLHA O TESTE:")
        print("1 - Teste com comando PRINT (diferentes codificações)")
        print("2 - Teste com cópia direta para porta")
        print("3 - Teste manual com Notepad")
        print("4 - Criar teste ESC/POS")
        print("0 - Sair")
        
        opcao = input("\nOpção: ")
        
        if opcao == '1':
            testar_impressao_metodo1(printer_name)
        elif opcao == '2':
            testar_impressao_metodo2(printer_name)
        elif opcao == '3':
            testar_impressao_metodo3(printer_name)
        elif opcao == '4':
            print("\nArquivo teste_escpos.txt criado.")
            print("Use um dos métodos acima para enviá-lo")
        elif opcao == '0':
            break

if __name__ == "__main__":
    main()