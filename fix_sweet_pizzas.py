#!/usr/bin/env python3
"""
Script para corrigir pizzas doces que estão incorretamente marcadas como promocionais.
Solução: Marcar as promocionais como inativas e garantir que existam versões regulares.
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoProject.settings')
django.setup()

from apps.produtos.models import Produto, ProdutoPreco, Categoria, Tamanho
from decimal import Decimal

def main():
    print("=== CORREÇÃO DE PIZZAS DOCES PROMOCIONAIS ===\n")
    
    # 1. Marcar pizzas doces promocionais como inativas
    pizzas_promo_doces = [
        {'id': 37, 'nome': 'Pizza Promocional Banana Caramelizada'},
        {'id': 38, 'nome': 'Pizza Promocional Abacaxi Gratinado'},
        {'id': 39, 'nome': 'Pizza Promocional Romeu e Julieta'}
    ]
    
    print("1. Marcando pizzas promocionais doces como inativas...")
    for pizza_info in pizzas_promo_doces:
        try:
            pizza = Produto.objects.get(id=pizza_info['id'])
            pizza.ativo = False
            pizza.save()
            print(f"   ✓ {pizza.nome} marcada como inativa")
        except Produto.DoesNotExist:
            print(f"   ⚠ Pizza ID {pizza_info['id']} não encontrada")
    
    # 2. Verificar e criar pizzas doces regulares
    categoria_doces = Categoria.objects.get(nome="Pizzas Doces")
    tamanhos = {
        'Pequena': Tamanho.objects.get(nome='Pequena'),
        'Média': Tamanho.objects.get(nome='Média'),
        'Grande': Tamanho.objects.get(nome='Grande'),
        'Família': Tamanho.objects.get(nome='Família')
    }
    
    pizzas_doces_regulares = [
        {
            'nome': 'Pizza Abacaxi Gratinado',
            'descricao': 'Molho de tomate, mussarela, abacaxi em calda, queijo coalho e orégano',
            'ingredientes': 'Molho de tomate, mussarela, abacaxi em calda, queijo coalho, orégano',
            'precos': {'Pequena': 24.00, 'Média': 34.00, 'Grande': 44.00, 'Família': 54.00}
        },
        {
            'nome': 'Pizza Banana Caramelizada',
            'descricao': 'Molho de tomate, mussarela, banana caramelizada, canela e açúcar',
            'ingredientes': 'Molho de tomate, mussarela, banana caramelizada, canela, açúcar',
            'precos': {'Pequena': 24.00, 'Média': 34.00, 'Grande': 44.00, 'Família': 54.00}
        },
        {
            'nome': 'Pizza Romeu e Julieta',
            'descricao': 'Molho de tomate, mussarela, goiabada e queijo minas',
            'ingredientes': 'Molho de tomate, mussarela, goiabada, queijo minas',
            'precos': {'Pequena': 26.00, 'Média': 36.00, 'Grande': 46.00, 'Família': 56.00}
        }
    ]
    
    print("\n2. Verificando e criando pizzas doces regulares...")
    for pizza_data in pizzas_doces_regulares:
        # Verificar se já existe
        existing = Produto.objects.filter(
            nome=pizza_data['nome'],
            categoria=categoria_doces,
            ativo=True
        ).first()
        
        if existing:
            print(f"   ✓ {pizza_data['nome']} já existe (ID: {existing.id})")
            # Verificar se os preços estão corretos
            for tamanho_nome, preco_esperado in pizza_data['precos'].items():
                preco_obj = ProdutoPreco.objects.filter(
                    produto=existing,
                    tamanho=tamanhos[tamanho_nome]
                ).first()
                
                if preco_obj:
                    if float(preco_obj.preco) != preco_esperado:
                        preco_obj.preco = Decimal(str(preco_esperado))
                        preco_obj.save()
                        print(f"     - Preço {tamanho_nome} atualizado: R$ {preco_esperado}")
                else:
                    # Criar preço faltante
                    ProdutoPreco.objects.create(
                        produto=existing,
                        tamanho=tamanhos[tamanho_nome],
                        preco=Decimal(str(preco_esperado))
                    )
                    print(f"     - Preço {tamanho_nome} criado: R$ {preco_esperado}")
        else:
            # Criar nova pizza
            nova_pizza = Produto.objects.create(
                nome=pizza_data['nome'],
                descricao=pizza_data['descricao'],
                categoria=categoria_doces,
                tipo_produto='pizza',
                ingredientes=pizza_data['ingredientes'],
                ativo=True
            )
            print(f"   ✓ {pizza_data['nome']} criada (ID: {nova_pizza.id})")
            
            # Criar preços
            for tamanho_nome, preco_valor in pizza_data['precos'].items():
                ProdutoPreco.objects.create(
                    produto=nova_pizza,
                    tamanho=tamanhos[tamanho_nome],
                    preco=Decimal(str(preco_valor))
                )
                print(f"     - Preço {tamanho_nome}: R$ {preco_valor}")
    
    print("\n=== CORREÇÃO CONCLUÍDA ===")
    print("\nVerificação final:")
    
    # Listar pizzas doces ativas
    pizzas_doces_ativas = Produto.objects.filter(
        categoria=categoria_doces,
        ativo=True
    ).values_list('id', 'nome')
    
    print(f"\nPizzas doces ativas ({len(pizzas_doces_ativas)}):")
    for pizza in pizzas_doces_ativas:
        print(f"  ID {pizza[0]}: {pizza[1]}")
    
    # Listar pizzas doces inativas (promocionais)
    pizzas_doces_inativas = Produto.objects.filter(
        categoria=categoria_doces,
        ativo=False
    ).values_list('id', 'nome')
    
    print(f"\nPizzas doces inativas/promocionais ({len(pizzas_doces_inativas)}):")
    for pizza in pizzas_doces_inativas:
        print(f"  ID {pizza[0]}: {pizza[1]}")

if __name__ == '__main__':
    main()