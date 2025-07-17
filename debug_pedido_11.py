#!/usr/bin/env python
import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoProject.settings')
django.setup()

from apps.pedidos.models import Pedido, ItemPedido

# Verificar pedido 11
try:
    pedido = Pedido.objects.get(numero='000011')
    print(f'Pedido: {pedido}')
    print(f'Cliente: {pedido.cliente.nome}')
    print(f'Total de itens: {pedido.itens.count()}')
    print('-' * 50)

    for item in pedido.itens.all():
        print(f'\nItem ID: {item.id}')
        if item.produto_preco:
            print(f'Produto: {item.produto_preco.produto.nome}')
            print(f'Categoria: {item.produto_preco.produto.categoria.nome if item.produto_preco.produto.categoria else "SEM CATEGORIA"}')
            print(f'Tamanho: {item.produto_preco.tamanho.nome if item.produto_preco.tamanho else "SEM TAMANHO"}')
        else:
            print('SEM PRODUTO_PRECO')
        
        print(f'É meio a meio: {item.is_meio_a_meio}')
        print(f'Meio a meio data: {item.meio_a_meio_data}')
        print(f'Quantidade: {item.quantidade}')
        print(f'Observações: {item.observacoes}')
        
except Pedido.DoesNotExist:
    print('Pedido 000011 não encontrado!')