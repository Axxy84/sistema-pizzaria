#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para testar impressão ESC/POS
"""
import sys
import os

# Adicionar path do projeto
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoProject.settings')
import django
django.setup()

from apps.pedidos.impressao_escpos import ImpressoraTermica, detectar_impressora_windows

def main():
    print("="*50)
    print("   TESTE DE IMPRESSAO ESC/POS")
    print("="*50)
    print()
    
    impressora = ImpressoraTermica()
    
    print("1. Detectando portas COM disponíveis...")
    portas = detectar_impressora_windows()
    if portas:
        print(f"   Portas encontradas: {', '.join(portas)}")
    else:
        print("   Nenhuma porta COM encontrada")
    
    print()
    print("2. Tentando conectar via USB...")
    resultado = impressora.conectar_usb()
    
    if isinstance(resultado, tuple) and not resultado[0]:
        print(f"   USB falhou: {resultado[1]}")
        print()
        print("3. Tentando portas COM/Serial...")
        
        conectado = False
        for porta in portas:
            print(f"   Testando {porta}...")
            try:
                if impressora.conectar_serial(porta, 9600):
                    print(f"   ✓ Conectado em {porta}")
                    conectado = True
                    break
            except Exception as e:
                print(f"   ✗ {porta} falhou: {e}")
        
        if not conectado:
            print()
            print("4. Usando modo DUMMY (simulação)...")
            impressora.conectar_dummy()
    else:
        print("   ✓ Conectado via USB!")
    
    print()
    print("5. Enviando impressão de teste...")
    
    try:
        impressora.imprimir_teste()
        print("   ✓ Teste enviado com sucesso!")
        
        if isinstance(impressora.printer, type(impressora.printer).__class__.__name__ == 'Dummy'):
            print()
            print("   Modo DUMMY - Conteúdo que seria impresso:")
            print("   " + "-"*40)
            print(impressora.printer.output)
            
    except Exception as e:
        print(f"   ✗ Erro: {e}")
    
    finally:
        impressora.desconectar()
    
    print()
    print("="*50)
    
    # Alternativa: usar porta USB diretamente
    print()
    print("ALTERNATIVA: Impressão direta via USB001/USB002")
    print("-"*50)
    
    if os.path.exists('knup_porta.txt'):
        with open('knup_porta.txt', 'r') as f:
            porta_usb = f.read().strip()
        print(f"Porta configurada: {porta_usb}")
        print("Use o sistema anterior que já está funcionando!")
    else:
        print("Execute primeiro: configurar_impressao_knup.bat")

if __name__ == "__main__":
    main()
    input("\nPressione ENTER para sair...")