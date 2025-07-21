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
print("🗑️  Iniciando limpeza do banco de dados...\n")

try:
    with transaction.atomic():
        # 1. Limpar Movimentações Financeiras
        print("Removendo movimentações financeiras...")
        mov_count = MovimentoCaixa.objects.count()
        conta_count = ContaPagar.objects.count()
        MovimentoCaixa.objects.all().delete()
        ContaPagar.objects.all().delete()
        print(f"  ✅ {mov_count} movimentações removidas")
        print(f"  ✅ {conta_count} contas a pagar removidas")
        
        # 2. Limpar Movimentações de Estoque
        print("\nRemovendo movimentações de estoque...")
        estoque_count = MovimentoEstoque.objects.count()
        MovimentoEstoque.objects.all().delete()
        print(f"  ✅ {estoque_count} movimentações de estoque removidas")
        
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
        caixas = Caixa.objects.all()
        for caixa in caixas:
            caixa.saldo_inicial = 0
            caixa.saldo_atual = 0
            caixa.total_entradas = 0
            caixa.total_saidas = 0
            caixa.save()
        print(f"  ✅ {caixas.count()} caixas resetados")
        
        print("\n✨ Limpeza concluída com sucesso!")
        
except Exception as e:
    print(f"\n❌ Erro durante a limpeza: {str(e)}")
    import traceback
    traceback.print_exc()
    exit(1)

# Mostrar estatísticas finais
print("\n📊 ESTATÍSTICAS FINAIS:")
print(f"  Pedidos: {Pedido.objects.count()}")
print(f"  Itens de Pedido: {ItemPedido.objects.count()}")
print(f"  Clientes: {Cliente.objects.count()}")
print(f"  Endereços: {Endereco.objects.count()}")
print(f"  Mesas: {Mesa.objects.count()}")
print(f"  Movimentações Financeiras: {MovimentoCaixa.objects.count()}")
print(f"  Movimentações de Estoque: {MovimentoEstoque.objects.count()}")

# Verificar produtos (não removemos produtos)
from apps.produtos.models import Produto
print(f"\n📦 Produtos disponíveis: {Produto.objects.count()}")

print("\n🎯 Sistema pronto para receber dados reais!")
print("\n📝 Próximos passos:")
print("1. Acesse /admin/ para criar clientes manualmente")
print("2. Ou use /pedidos/rapido/ para criar pedidos sem cliente")
print("3. Abra o caixa do dia em /financeiro/caixa/")
print("4. Crie pedidos e teste o fluxo: Recebido → Preparando → Entregue")
print("5. Para cancelar pedidos, use a senha: 1234")