#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Teste simples de impressão de cupom
"""
import sys
import os

# Adicionar path do projeto
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from apps.pedidos.cupom_printer import gerar_cupom_texto, salvar_cupom_arquivo, imprimir_cupom_windows

# Dados de teste
pedido_teste = {
    'numero': '000007',
    'cliente': 'José da Silva',
    'tipo': 'Balcão',
    'itens': [
        {
            'nome': 'Pizza Camarão Premium',
            'descricao': 'Camarões frescos, catupiry e mussarela',
            'quantidade': 1,
            'valor': 65.00
        },
        {
            'nome': 'Coca-Cola 2L',
            'descricao': '',
            'quantidade': 1,
            'valor': 12.00
        }
    ],
    'observacoes': 'Sem cebola na pizza'
}

def main():
    print("="*50)
    print("   TESTE DE IMPRESSAO DE CUPOM SIMPLES")
    print("="*50)
    print()
    
    # Gerar cupom
    print("1. Gerando cupom em texto...")
    cupom = gerar_cupom_texto(pedido_teste)
    print(cupom)
    print()
    
    # Salvar arquivo
    print("2. Salvando em arquivo...")
    arquivo = salvar_cupom_arquivo(pedido_teste, "cupom_teste.txt")
    print(f"   Arquivo salvo: {arquivo}")
    print()
    
    # Perguntar se quer imprimir
    resp = input("3. Deseja imprimir o cupom? (s/n): ")
    if resp.lower() == 's':
        print()
        print("   Enviando para impressora...")
        imprimir_cupom_windows(pedido_teste)
        print("   Comando enviado!")
    
    print()
    print("="*50)
    print("DICAS:")
    print("- Se continuar com problemas, use driver Generic/Text Only")
    print("- Configure a impressora para modo texto/raw")
    print("- Evite acentos e caracteres especiais")
    print("="*50)

if __name__ == "__main__":
    main()
    input("\nPressione ENTER para sair...")