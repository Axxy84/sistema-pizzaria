#!/usr/bin/env python
import os
import sys

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoProject.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import django
django.setup()

from django.db import transaction
from apps.pedidos.models import Pedido, ItemPedido
from apps.pedidos.models_mesa import Mesa
from apps.clientes.models import Cliente, Endereco
from apps.financeiro.models import MovimentoCaixa, Caixa, ContaPagar
from apps.estoque.models import MovimentoEstoque

print("=== RESETANDO BANCO DE DADOS PARA TESTES REAIS ===\n")

# Confirmação de segurança
resposta = input("⚠️  ATENÇÃO: Isso vai APAGAR todos os pedidos, clientes e movimentações!\nTem certeza? (digite 'SIM' para confirmar): ")

if resposta != 'SIM':
    print("\nOperação cancelada.")
    exit(0)

print("\n🗑️  Iniciando limpeza do banco de dados...\n")

try:
    with transaction.atomic():
        # 1. Limpar Movimentações Financeiras
        print("Removendo movimentações financeiras...")
        MovimentoCaixa.objects.all().delete()
        ContaPagar.objects.all().delete()
        print(f"  ✅ Movimentações financeiras removidas")
        
        # 2. Limpar Movimentações de Estoque
        print("\nRemovendo movimentações de estoque...")
        MovimentoEstoque.objects.all().delete()
        print(f"  ✅ Movimentações de estoque removidas")
        
        # 3. Limpar Itens de Pedido
        print("\nRemovendo itens de pedidos...")
        itens_count = ItemPedido.objects.count()
        ItemPedido.objects.all().delete()
        print(f"  ✅ {itens_count} itens de pedido removidos")
        
        # 4. Limpar Pedidos
        print("\nRemovendo pedidos...")
        pedidos_count = Pedido.objects.count()
        Pedido.objects.all().delete()
        print(f"  ✅ {pedidos_count} pedidos removidos")
        
        # 5. Limpar Mesas
        print("\nRemovendo mesas...")
        mesas_count = Mesa.objects.count()
        Mesa.objects.all().delete()
        print(f"  ✅ {mesas_count} mesas removidas")
        
        # 6. Limpar Endereços e Clientes
        print("\nRemovendo clientes e endereços...")
        enderecos_count = Endereco.objects.count()
        clientes_count = Cliente.objects.count()
        Endereco.objects.all().delete()
        Cliente.objects.all().delete()
        print(f"  ✅ {clientes_count} clientes removidos")
        print(f"  ✅ {enderecos_count} endereços removidos")
        
        # 7. Resetar Caixas
        print("\nResetando caixas...")
        Caixa.objects.all().update(
            saldo_inicial=0,
            saldo_atual=0,
            total_entradas=0,
            total_saidas=0
        )
        print(f"  ✅ Caixas resetados")
        
        print("\n✨ Limpeza concluída com sucesso!")
        
except Exception as e:
    print(f"\n❌ Erro durante a limpeza: {str(e)}")
    exit(1)

# Mostrar estatísticas finais
print("\n📊 ESTATÍSTICAS FINAIS:")
print(f"  Pedidos: {Pedido.objects.count()}")
print(f"  Clientes: {Cliente.objects.count()}")
print(f"  Mesas: {Mesa.objects.count()}")
print(f"  Movimentações Financeiras: {MovimentoCaixa.objects.count()}")
print(f"  Movimentações de Estoque: {MovimentoEstoque.objects.count()}")

print("\n🎯 Sistema pronto para receber dados reais!")
print("\nDicas para começar:")
print("1. Crie alguns clientes de teste")
print("2. Abra o caixa do dia")
print("3. Crie pedidos com dados reais")
print("4. Teste o fluxo completo: Recebido → Preparando → Entregue")