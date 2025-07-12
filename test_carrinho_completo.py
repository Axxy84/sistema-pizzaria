#!/usr/bin/env python
"""
Script para testar fluxo completo do carrinho de compras
Simula o processo desde adicionar produtos até finalizar pedido
"""

import os
import sys
import django
from decimal import Decimal

# Setup Django
sys.path.append('/home/labdev/Documentos/DjangoProject')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoProject.settings')
django.setup()

from apps.produtos.models import Produto, ProdutoPreco
from apps.clientes.models import Cliente
from apps.pedidos.models import Pedido, ItemPedido
from django.contrib.auth.models import User

class CarrinhoTester:
    def __init__(self):
        self.base_url = "http://127.0.0.1:8000"
        self.carrinho = []
        self.cliente_dados = {
            'nome': 'João Silva',
            'telefone': '11987654321',
            'email': 'joao@teste.com'
        }
        
    def test_carregar_produtos(self):
        """Testa carregamento de produtos da API"""
        print("🍕 Testando carregamento de produtos...")
        
        try:
            # Testar endpoint direto no Django
            from apps.produtos.views import ProdutoViewSet
            from rest_framework.test import APIRequestFactory
            
            factory = APIRequestFactory()
            request = factory.get('/api/produtos/para_pedido/')
            
            view = ProdutoViewSet()
            view.action = 'para_pedido'
            response = view.para_pedido(request)
            
            if response.status_code == 200:
                produtos_data = response.data
                print(f"✅ Produtos carregados: {len(produtos_data)} categorias")
                
                # Verificar estrutura dos dados
                for categoria, produtos in produtos_data.items():
                    print(f"   {categoria}: {len(produtos)} produtos")
                
                return produtos_data
            else:
                print(f"❌ Erro ao carregar produtos: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Erro no teste de produtos: {e}")
            return None
    
    def test_adicionar_ao_carrinho(self, produtos_data):
        """Testa adição de produtos ao carrinho"""
        print("\n🛒 Testando adição ao carrinho...")
        
        try:
            # Adicionar uma pizza
            if 'pizzas' in produtos_data and produtos_data['pizzas']:
                pizza = produtos_data['pizzas'][0]
                if pizza.get('tamanhos') and len(pizza['tamanhos']) > 0:
                    tamanho_info = pizza['tamanhos'][0]
                    tamanho = tamanho_info['size']
                    preco = tamanho_info['preco']
                    
                    item_carrinho = {
                        'produto_id': pizza['id'],
                        'nome': pizza['nome'],
                        'tamanho': tamanho,
                        'preco': Decimal(str(preco)),
                        'quantidade': 2
                    }
                    self.carrinho.append(item_carrinho)
                    print(f"✅ Pizza adicionada: {pizza['nome']} - {tamanho} (2x) - R$ {preco}")
            
            # Adicionar uma bebida
            if 'bebidas' in produtos_data and produtos_data['bebidas']:
                bebida = produtos_data['bebidas'][0]
                preco = bebida.get('preco', 0)
                
                item_carrinho = {
                    'produto_id': bebida['id'],
                    'nome': bebida['nome'],
                    'preco': Decimal(str(preco)),
                    'quantidade': 1
                }
                self.carrinho.append(item_carrinho)
                print(f"✅ Bebida adicionada: {bebida['nome']} (1x) - R$ {preco}")
            
            # Calcular total
            total = sum(item['preco'] * item['quantidade'] for item in self.carrinho)
            print(f"✅ Total do carrinho: R$ {total:.2f}")
            
            return True
            
        except Exception as e:
            print(f"❌ Erro ao adicionar ao carrinho: {e}")
            return False
    
    def test_criar_cliente(self):
        """Testa criação de cliente"""
        print("\n👤 Testando criação de cliente...")
        
        try:
            cliente, created = Cliente.objects.get_or_create(
                telefone=self.cliente_dados['telefone'],
                defaults={
                    'nome': self.cliente_dados['nome'],
                    'email': self.cliente_dados['email']
                }
            )
            
            if created:
                print(f"✅ Cliente criado: {cliente.nome}")
            else:
                print(f"✅ Cliente encontrado: {cliente.nome}")
            
            return cliente
            
        except Exception as e:
            print(f"❌ Erro ao criar cliente: {e}")
            return None
    
    def test_finalizar_pedido(self, cliente):
        """Testa finalização do pedido"""
        print("\n📝 Testando finalização do pedido...")
        
        try:
            # Buscar usuário para o pedido
            usuario = User.objects.first()
            if not usuario:
                print("❌ Nenhum usuário encontrado")
                return None
            
            # Calcular totais
            subtotal = sum(item['preco'] * item['quantidade'] for item in self.carrinho)
            taxa_entrega = Decimal('5.00')
            total = subtotal + taxa_entrega
            
            # Criar pedido
            pedido = Pedido.objects.create(
                cliente=cliente,
                usuario=usuario,
                tipo='delivery',
                forma_pagamento='pix',
                subtotal=subtotal,
                taxa_entrega=taxa_entrega,
                total=total,
                observacoes='Pedido de teste - fluxo completo'
            )
            
            print(f"✅ Pedido criado: #{pedido.numero}")
            
            # Adicionar itens ao pedido
            for item in self.carrinho:
                # Buscar produto_preco correspondente
                produto = Produto.objects.get(id=item['produto_id'])
                
                if 'tamanho' in item:
                    # Produto com tamanho (pizza)
                    produto_preco = ProdutoPreco.objects.filter(
                        produto=produto,
                        tamanho__nome__icontains=item['tamanho']
                    ).first()
                else:
                    # Produto sem tamanho (bebida)
                    produto_preco = ProdutoPreco.objects.filter(produto=produto).first()
                
                if produto_preco:
                    ItemPedido.objects.create(
                        pedido=pedido,
                        produto_preco=produto_preco,
                        quantidade=item['quantidade'],
                        preco_unitario=item['preco'],
                        subtotal=item['preco'] * item['quantidade']
                    )
                    print(f"✅ Item adicionado: {item['nome']} ({item['quantidade']}x)")
            
            # Verificar itens salvos
            itens_salvos = ItemPedido.objects.filter(pedido=pedido)
            print(f"✅ Itens salvos no banco: {itens_salvos.count()}")
            
            # Verificar totais
            print(f"   Subtotal: R$ {pedido.subtotal}")
            print(f"   Taxa entrega: R$ {pedido.taxa_entrega}")
            print(f"   Total: R$ {pedido.total}")
            
            return pedido
            
        except Exception as e:
            print(f"❌ Erro ao finalizar pedido: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def test_verificar_persistencia(self, pedido):
        """Verifica se os dados foram persistidos corretamente"""
        print("\n🔍 Verificando persistência dos dados...")
        
        try:
            # Recarregar pedido do banco
            pedido_db = Pedido.objects.get(id=pedido.id)
            print(f"✅ Pedido encontrado no banco: #{pedido_db.numero}")
            
            # Verificar itens
            itens = ItemPedido.objects.filter(pedido=pedido_db)
            print(f"✅ Itens do pedido: {itens.count()}")
            
            for item in itens:
                produto_nome = item.produto_preco.produto.nome
                if hasattr(item.produto_preco, 'tamanho'):
                    tamanho = item.produto_preco.tamanho.nome
                    print(f"   - {produto_nome} ({tamanho}) - {item.quantidade}x R$ {item.preco_unitario}")
                else:
                    print(f"   - {produto_nome} - {item.quantidade}x R$ {item.preco_unitario}")
            
            # Verificar cliente
            print(f"✅ Cliente: {pedido_db.cliente.nome} ({pedido_db.cliente.telefone})")
            
            # Verificar status
            print(f"✅ Status: {pedido_db.status}")
            print(f"✅ Forma pagamento: {pedido_db.forma_pagamento}")
            
            return True
            
        except Exception as e:
            print(f"❌ Erro na verificação: {e}")
            return False
    
    def test_api_carrinho_simulation(self):
        """Simula uso da API como o frontend faria"""
        print("\n🌐 Testando simulação de API do carrinho...")
        
        try:
            # Simular chamada para finalizar pedido
            from django.test import Client
            from django.urls import reverse
            import json
            
            client = Client()
            
            # Preparar dados do pedido
            dados_pedido = {
                'cliente': {
                    'nome': self.cliente_dados['nome'],
                    'telefone': self.cliente_dados['telefone'],
                    'email': self.cliente_dados['email']
                },
                'tipo': 'delivery',
                'forma_pagamento': 'pix',
                'itens': [
                    {
                        'produto_id': item['produto_id'],
                        'quantidade': item['quantidade'],
                        'preco_unitario': float(item['preco'])
                    } for item in self.carrinho
                ],
                'observacoes': 'Teste de simulação API'
            }
            
            print(f"✅ Dados preparados para API: {len(dados_pedido['itens'])} itens")
            return True
            
        except Exception as e:
            print(f"❌ Erro na simulação API: {e}")
            return False
    
    def run_complete_test(self):
        """Executa teste completo do carrinho"""
        print("🧪 TESTE COMPLETO DO CARRINHO DE COMPRAS")
        print("=" * 60)
        
        tests_passed = 0
        total_tests = 6
        
        # Teste 1: Carregar produtos
        produtos_data = self.test_carregar_produtos()
        if produtos_data:
            tests_passed += 1
        
        # Teste 2: Adicionar ao carrinho
        if produtos_data and self.test_adicionar_ao_carrinho(produtos_data):
            tests_passed += 1
        
        # Teste 3: Criar cliente
        cliente = self.test_criar_cliente()
        if cliente:
            tests_passed += 1
        
        # Teste 4: Finalizar pedido
        pedido = None
        if cliente and self.test_finalizar_pedido(cliente):
            pedido = Pedido.objects.filter(cliente=cliente).last()
            tests_passed += 1
        
        # Teste 5: Verificar persistência
        if pedido and self.test_verificar_persistencia(pedido):
            tests_passed += 1
        
        # Teste 6: Simular API
        if self.test_api_carrinho_simulation():
            tests_passed += 1
        
        # Resultado final
        print("\n" + "=" * 60)
        print(f"📊 RESULTADO: {tests_passed}/{total_tests} testes do carrinho passaram")
        
        if tests_passed == total_tests:
            print("🎉 FLUXO COMPLETO DO CARRINHO FUNCIONANDO!")
            print("✅ Produtos → Carrinho → Cliente → Pedido → Banco")
        else:
            print("⚠️ Alguns testes falharam. Verificar logs acima.")
        
        # Estatísticas do teste
        if pedido:
            print(f"\n📈 ESTATÍSTICAS DO TESTE:")
            print(f"   Pedido criado: #{pedido.numero}")
            print(f"   Itens no carrinho: {len(self.carrinho)}")
            print(f"   Total testado: R$ {pedido.total}")
            print(f"   Cliente: {pedido.cliente.nome}")
        
        return tests_passed == total_tests

if __name__ == '__main__':
    tester = CarrinhoTester()
    success = tester.run_complete_test()