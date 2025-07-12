#!/usr/bin/env python
"""
Script para testar operações CRUD básicas com Supabase
Verifica se a integração está funcionando corretamente
"""

import os
import sys
import django
from decimal import Decimal
from datetime import datetime

# Setup Django
sys.path.append('/home/labdev/Documentos/DjangoProject')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoProject.settings')
django.setup()

from apps.produtos.models import Produto, Categoria, Tamanho, ProdutoPreco
from apps.clientes.models import Cliente, Endereco
from apps.pedidos.models import Pedido, ItemPedido
from django.contrib.auth.models import User
from services.supabase_client import get_supabase_client

def test_supabase_connection():
    """Testa conexão básica com Supabase"""
    print("🔗 Testando conexão com Supabase...")
    try:
        supabase = get_supabase_client()
        # Testa uma query simples
        result = supabase.table('produtos_produto').select('count').execute()
        print(f"✅ Conexão OK - Produtos encontrados: {len(result.data) if result.data else 0}")
        return True
    except Exception as e:
        print(f"❌ Erro na conexão: {e}")
        return False

def test_produtos_crud():
    """Testa operações CRUD em produtos"""
    print("\n📦 Testando CRUD de Produtos...")
    
    try:
        # Listar produtos
        produtos = Produto.objects.filter(ativo=True)
        print(f"✅ Listagem - Produtos ativos: {produtos.count()}")
        
        # Verificar estrutura de um produto
        if produtos.exists():
            produto = produtos.first()
            print(f"✅ Produto exemplo: {produto.nome}")
            print(f"   - Categoria: {produto.categoria}")
            print(f"   - Tipo: {produto.tipo_produto}")
            print(f"   - Preços: {produto.tamanhos_precos}")
            
            # Verificar preços por tamanho
            precos = ProdutoPreco.objects.filter(produto=produto)
            print(f"   - Variações de preço: {precos.count()}")
            for preco in precos[:3]:  # Mostra só 3
                print(f"     {preco.tamanho.nome}: R$ {preco.preco}")
        
        return True
    except Exception as e:
        print(f"❌ Erro em produtos: {e}")
        return False

def test_clientes_crud():
    """Testa operações CRUD em clientes"""
    print("\n👥 Testando CRUD de Clientes...")
    
    try:
        # Criar cliente de teste
        cliente_teste, created = Cliente.objects.get_or_create(
            telefone='11999999999',
            defaults={
                'nome': 'Cliente Teste Supabase',
                'email': 'teste@supabase.com'
            }
        )
        
        if created:
            print("✅ Cliente de teste criado")
        else:
            print("✅ Cliente de teste já existe")
        
        # Criar endereço de teste
        endereco_teste, created = Endereco.objects.get_or_create(
            cliente=cliente_teste,
            tipo='casa',
            defaults={
                'cep': '01234-567',
                'logradouro': 'Rua de Teste',
                'numero': '123',
                'bairro': 'Bairro Teste',
                'cidade': 'São Paulo',
                'estado': 'SP',
                'principal': True
            }
        )
        
        if created:
            print("✅ Endereço de teste criado")
        else:
            print("✅ Endereço de teste já existe")
        
        print(f"   Cliente: {cliente_teste.nome} ({cliente_teste.telefone})")
        print(f"   Endereços: {cliente_teste.enderecos.count()}")
        
        return cliente_teste
    except Exception as e:
        print(f"❌ Erro em clientes: {e}")
        return None

def test_pedidos_crud(cliente_teste):
    """Testa operações CRUD em pedidos"""
    print("\n🛒 Testando CRUD de Pedidos...")
    
    try:
        # Buscar usuário admin
        try:
            usuario = User.objects.filter(is_superuser=True).first()
            if not usuario:
                usuario = User.objects.first()
            if not usuario:
                print("❌ Nenhum usuário encontrado para criar pedido")
                return False
        except:
            print("❌ Erro ao buscar usuário")
            return False
        
        # Buscar produto para teste
        produto = Produto.objects.filter(ativo=True, tipo_produto='pizza').first()
        if not produto:
            print("❌ Nenhuma pizza encontrada para teste")
            return False
        
        # Buscar preço do produto
        produto_preco = ProdutoPreco.objects.filter(produto=produto).first()
        if not produto_preco:
            print("❌ Nenhum preço encontrado para o produto")
            return False
        
        # Criar pedido de teste
        pedido = Pedido.objects.create(
            cliente=cliente_teste,
            usuario=usuario,
            tipo='delivery',
            forma_pagamento='pix',
            endereco_entrega=cliente_teste.enderecos.first(),
            observacoes='Pedido de teste - integração Supabase'
        )
        
        print(f"✅ Pedido criado: #{pedido.numero}")
        
        # Adicionar item ao pedido
        item = ItemPedido.objects.create(
            pedido=pedido,
            produto_preco=produto_preco,
            quantidade=1,
            preco_unitario=produto_preco.preco,
            subtotal=produto_preco.preco
        )
        
        print(f"✅ Item adicionado: {produto.nome} - {produto_preco.tamanho.nome}")
        
        # Atualizar totais do pedido
        pedido.subtotal = item.subtotal
        pedido.taxa_entrega = Decimal('5.00')
        pedido.total = pedido.subtotal + pedido.taxa_entrega
        pedido.save()
        
        print(f"   Subtotal: R$ {pedido.subtotal}")
        print(f"   Taxa entrega: R$ {pedido.taxa_entrega}")
        print(f"   Total: R$ {pedido.total}")
        
        # Verificar se foi salvo no banco
        pedido_db = Pedido.objects.get(id=pedido.id)
        print(f"✅ Pedido verificado no banco: {pedido_db.numero}")
        
        return pedido
    except Exception as e:
        print(f"❌ Erro em pedidos: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_supabase_direct_query():
    """Testa query direta no Supabase"""
    print("\n🔍 Testando query direta no Supabase...")
    
    try:
        supabase = get_supabase_client()
        
        # Buscar últimos pedidos
        result = supabase.table('pedidos_pedido').select('*').order('criado_em', desc=True).limit(5).execute()
        
        print(f"✅ Últimos 5 pedidos encontrados: {len(result.data)}")
        for pedido in result.data:
            print(f"   #{pedido.get('numero')} - {pedido.get('cliente_id')} - R$ {pedido.get('total')}")
        
        # Buscar produtos ativos
        result = supabase.table('produtos_produto').select('nome, tipo_produto, ativo').eq('ativo', True).execute()
        print(f"✅ Produtos ativos no Supabase: {len(result.data)}")
        
        return True
    except Exception as e:
        print(f"❌ Erro na query direta: {e}")
        return False

def run_all_tests():
    """Executa todos os testes"""
    print("🧪 TESTE DE INTEGRAÇÃO SUPABASE - CRUD BÁSICO")
    print("=" * 60)
    
    tests_passed = 0
    total_tests = 5
    
    # Teste 1: Conexão
    if test_supabase_connection():
        tests_passed += 1
    
    # Teste 2: Produtos
    if test_produtos_crud():
        tests_passed += 1
    
    # Teste 3: Clientes
    cliente_teste = test_clientes_crud()
    if cliente_teste:
        tests_passed += 1
    
    # Teste 4: Pedidos
    if cliente_teste and test_pedidos_crud(cliente_teste):
        tests_passed += 1
    
    # Teste 5: Query direta
    if test_supabase_direct_query():
        tests_passed += 1
    
    # Resultado final
    print("\n" + "=" * 60)
    print(f"📊 RESULTADO: {tests_passed}/{total_tests} testes passaram")
    
    if tests_passed == total_tests:
        print("🎉 TODAS AS OPERAÇÕES CRUD FUNCIONANDO CORRETAMENTE!")
    else:
        print("⚠️  Alguns testes falharam. Verificar logs acima.")
    
    return tests_passed == total_tests

if __name__ == '__main__':
    run_all_tests()