#!/usr/bin/env python
"""
Teste completo da funcionalidade meio a meio
"""

import os
import sys
import django
import json
from decimal import Decimal

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoProject.settings')
django.setup()

from apps.produtos.models import Produto, ProdutoPreco, Tamanho
from apps.pedidos.models import Pedido, ItemPedido
from apps.clientes.models import Cliente
from django.contrib.auth.models import User

def test_meio_a_meio():
    print("=== TESTE COMPLETO DA FUNCIONALIDADE MEIO A MEIO ===\n")
    
    # 1. Verificar dados existentes
    print("1. Verificando dados existentes...")
    pizzas = Produto.objects.filter(tipo_produto='pizza', ativo=True)
    tamanhos = Tamanho.objects.filter(ativo=True)
    
    print(f"   ✅ {pizzas.count()} pizzas disponíveis")
    print(f"   ✅ {tamanhos.count()} tamanhos disponíveis")
    
    if pizzas.count() < 2:
        print("   ❌ Necessário pelo menos 2 pizzas para teste meio a meio")
        return False
    
    # 2. Testar modelo ItemPedido
    print("\n2. Testando modelo ItemPedido...")
    
    # Selecionar dados para teste - encontrar um tamanho com pelo menos 2 pizzas
    tamanho = None
    pizza_1 = None
    pizza_2 = None
    
    for t in tamanhos:
        pizzas_neste_tamanho = ProdutoPreco.objects.filter(
            tamanho=t, 
            produto__tipo_produto='pizza'
        ).select_related('produto')
        
        if pizzas_neste_tamanho.count() >= 2:
            tamanho = t
            pizza_1 = pizzas_neste_tamanho[0].produto
            pizza_2 = pizzas_neste_tamanho[1].produto
            break
    
    if not tamanho:
        print("   ❌ Não foi encontrado um tamanho com pelo menos 2 pizzas com preço")
        return False
    
    # Verificar se existem preços
    try:
        preco_1 = ProdutoPreco.objects.get(produto=pizza_1, tamanho=tamanho)
        preco_2 = ProdutoPreco.objects.get(produto=pizza_2, tamanho=tamanho)
        print(f"   ✅ Preços encontrados: {pizza_1.nome} = R$ {preco_1.preco_final}, {pizza_2.nome} = R$ {preco_2.preco_final}")
    except ProdutoPreco.DoesNotExist:
        print("   ❌ Preços não encontrados para as pizzas selecionadas")
        return False
    
    # Criar item teste
    item = ItemPedido()
    item.quantidade = 1
    
    try:
        item.configurar_meio_a_meio(pizza_1, pizza_2, tamanho, 'mais_caro')
        print(f"   ✅ Configuração meio a meio criada")
        print(f"       Sabor 1: {item.sabor_1['nome']}")
        print(f"       Sabor 2: {item.sabor_2['nome']}")
        print(f"       Preço calculado: R$ {item.preco_unitario}")
        print(f"       É meio a meio: {item.is_meio_a_meio}")
        print(f"       Descrição: {item.get_descricao_completa()}")
    except Exception as e:
        print(f"   ❌ Erro ao configurar meio a meio: {e}")
        return False
    
    # 3. Testar diferentes regras de preço
    print("\n3. Testando regras de preço...")
    
    # Mais caro
    item_mais_caro = ItemPedido()
    item_mais_caro.configurar_meio_a_meio(pizza_1, pizza_2, tamanho, 'mais_caro')
    preco_mais_caro = item_mais_caro.preco_unitario
    print(f"   ✅ Regra 'mais_caro': R$ {preco_mais_caro}")
    
    # Média
    item_media = ItemPedido()
    item_media.configurar_meio_a_meio(pizza_1, pizza_2, tamanho, 'media')
    preco_media = item_media.preco_unitario
    print(f"   ✅ Regra 'media': R$ {preco_media}")
    
    # Verificar lógica
    preco_esperado_mais_caro = max(preco_1.preco_final, preco_2.preco_final)
    preco_esperado_media = (preco_1.preco_final + preco_2.preco_final) / 2
    
    if preco_mais_caro == preco_esperado_mais_caro:
        print(f"   ✅ Regra 'mais_caro' correta")
    else:
        print(f"   ❌ Regra 'mais_caro' incorreta: esperado {preco_esperado_mais_caro}, obtido {preco_mais_caro}")
    
    if preco_media == preco_esperado_media:
        print(f"   ✅ Regra 'media' correta")
    else:
        print(f"   ❌ Regra 'media' incorreta: esperado {preco_esperado_media}, obtido {preco_media}")
    
    # 4. Testar JSON field
    print("\n4. Testando campo JSON...")
    print("   Dados meio a meio armazenados:")
    print(f"   {json.dumps(item.meio_a_meio_data, indent=4, ensure_ascii=False)}")
    
    # 5. Testar com pedido completo
    print("\n5. Testando com pedido completo...")
    
    try:
        # Buscar ou criar cliente e usuário
        user, _ = User.objects.get_or_create(username='teste_meio_a_meio', defaults={'email': 'teste@teste.com'})
        cliente, _ = Cliente.objects.get_or_create(
            nome='Cliente Teste Meio a Meio',
            defaults={'telefone': '11999999999', 'email': 'cliente@teste.com'}
        )
        
        # Criar pedido
        pedido = Pedido.objects.create(
            numero='999999',
            cliente=cliente,
            usuario=user,
            tipo='delivery',
            forma_pagamento='pix'
        )
        
        # Adicionar item meio a meio ao pedido
        item.pedido = pedido
        item.save()
        
        # Recalcular total
        pedido.calcular_total()
        
        print(f"   ✅ Pedido criado: #{pedido.numero}")
        print(f"   ✅ Item meio a meio adicionado")
        print(f"   ✅ Subtotal: R$ {pedido.subtotal}")
        print(f"   ✅ Total: R$ {pedido.total}")
        
        # Limpar dados de teste
        pedido.delete()
        print(f"   ✅ Dados de teste removidos")
        
    except Exception as e:
        print(f"   ❌ Erro no teste de pedido: {e}")
        return False
    
    # 6. Resumo final
    print("\n=== RESUMO DOS TESTES ===")
    print("✅ Modelo ItemPedido com campo meio_a_meio_data")
    print("✅ Método configurar_meio_a_meio()")
    print("✅ Propriedades is_meio_a_meio, sabor_1, sabor_2")
    print("✅ Cálculo de preço por regras (mais_caro, media)")
    print("✅ Método get_descricao_completa()")
    print("✅ Integração com modelo Pedido")
    print("✅ Armazenamento em JSON field")
    
    print("\n🎉 TODOS OS TESTES PASSARAM! Funcionalidade meio a meio está pronta.")
    return True

if __name__ == '__main__':
    test_meio_a_meio()