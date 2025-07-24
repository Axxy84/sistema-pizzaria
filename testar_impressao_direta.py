#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para testar impressão direta na impressora térmica
"""
import win32print
import win32ui
import win32con
import sys

def listar_impressoras():
    """Lista todas as impressoras instaladas"""
    print("\n=== IMPRESSORAS INSTALADAS ===")
    printers = win32print.EnumPrinters(2)
    for i, (flags, desc, name, comment) in enumerate(printers):
        print(f"{i+1}. {name}")
        if 'knup' in name.lower() or 'kp-im' in name.lower() or '609' in name.lower():
            print(f"   >>> KNUP DETECTADA!")
    return printers

def testar_impressao_simples(printer_name):
    """Testa impressão simples de texto"""
    try:
        print(f"\nTestando impressão em: {printer_name}")
        
        # Abrir impressora
        hprinter = win32print.OpenPrinter(printer_name)
        
        # Dados de teste
        raw_data = b"""

================================
      TESTE DE IMPRESSAO
      KNUP KP-IM609
================================

Data/Hora: Sistema Pizzaria
Pedido: #TESTE

--------------------------------
ITEM              QTD    VALOR
--------------------------------
Pizza Grande       1     45.00
Refrigerante       2      6.00
--------------------------------
TOTAL:                   51.00
--------------------------------

    OBRIGADO PELA PREFERENCIA!

================================



"""
        
        # Enviar dados
        hJob = win32print.StartDocPrinter(hprinter, 1, ("Teste Direto", None, "RAW"))
        win32print.StartPagePrinter(hprinter)
        win32print.WritePrinter(hprinter, raw_data)
        win32print.EndPagePrinter(hprinter)
        win32print.EndDocPrinter(hprinter)
        win32print.ClosePrinter(hprinter)
        
        print("✓ Comando enviado com sucesso!")
        print("  Verifique se a impressora imprimiu")
        
    except Exception as e:
        print(f"✗ Erro: {e}")

def testar_impressao_win32ui(printer_name):
    """Testa impressão usando Win32 UI"""
    try:
        print(f"\nTestando impressão Win32UI em: {printer_name}")
        
        # Criar DC da impressora
        hDC = win32ui.CreateDC()
        hDC.CreatePrinterDC(printer_name)
        
        # Iniciar documento
        hDC.StartDoc("Teste Win32UI")
        hDC.StartPage()
        
        # Configurar fonte
        font = win32ui.CreateFont({
            "name": "Courier New",
            "height": 20,
            "weight": 400,
        })
        hDC.SelectObject(font)
        
        # Imprimir texto
        y = 100
        hDC.TextOut(100, y, "=== TESTE IMPRESSORA TERMICA ===")
        y += 30
        hDC.TextOut(100, y, "KNUP KP-IM609")
        y += 30
        hDC.TextOut(100, y, "Sistema Pizzaria")
        y += 50
        hDC.TextOut(100, y, "Se você pode ler isso,")
        y += 30
        hDC.TextOut(100, y, "a impressora está funcionando!")
        
        # Finalizar
        hDC.EndPage()
        hDC.EndDoc()
        hDC.DeleteDC()
        
        print("✓ Documento enviado com sucesso!")
        
    except Exception as e:
        print(f"✗ Erro: {e}")

def main():
    print("="*50)
    print("   TESTE DE IMPRESSORA TERMICA KNUP")
    print("="*50)
    
    # Listar impressoras
    printers = listar_impressoras()
    
    if not printers:
        print("\nNenhuma impressora encontrada!")
        return
    
    # Procurar KNUP automaticamente
    knup_printer = None
    for flags, desc, name, comment in printers:
        if 'knup' in name.lower() or 'kp-im' in name.lower() or '609' in name.lower():
            knup_printer = name
            break
    
    if knup_printer:
        print(f"\n✓ KNUP encontrada: {knup_printer}")
        print("\nTestando impressão...")
        
        # Teste 1: Impressão RAW
        testar_impressao_simples(knup_printer)
        
        # Teste 2: Impressão Win32UI
        resp = input("\nTestar método alternativo? (s/n): ")
        if resp.lower() == 's':
            testar_impressao_win32ui(knup_printer)
    else:
        print("\n✗ Impressora KNUP não encontrada!")
        print("  Verifique se está instalada corretamente")
        
        # Permitir seleção manual
        try:
            num = int(input("\nDigite o número da impressora para testar: "))
            if 1 <= num <= len(printers):
                printer_name = printers[num-1][2]
                testar_impressao_simples(printer_name)
        except:
            pass

if __name__ == "__main__":
    try:
        import win32print
        import win32ui
    except ImportError:
        print("\n✗ ERRO: Módulo pywin32 não instalado!")
        print("  Execute: pip install pywin32")
        sys.exit(1)
    
    main()
    input("\nPressione ENTER para sair...")