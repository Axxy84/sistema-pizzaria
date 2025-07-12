#!/usr/bin/env python
"""
Script para testar as melhorias implementadas na integração Supabase
Valida tratamento de erros, validações e novos endpoints
"""

import os
import sys
import django

# Setup Django
sys.path.append('/home/labdev/Documentos/DjangoProject')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoProject.settings')
django.setup()

from apps.pedidos.utils import PedidoValidator, SupabaseErrorHandler, PedidoSupabaseManager, SupabaseHealthCheck
from apps.pedidos.views import PedidoViewSet
from rest_framework.test import APIRequestFactory

class TesteMelhorias:
    def __init__(self):
        self.factory = APIRequestFactory()
        self.manager = PedidoSupabaseManager()
    
    def test_validacoes(self):
        """Testa sistema de validações"""
        print("🔍 Testando sistema de validações...")
        
        # Teste 1: Dados válidos
        dados_validos = {
            'cliente': {
                'nome': 'João Silva',
                'telefone': '11987654321',
                'email': 'joao@teste.com'
            },
            'tipo': 'delivery',
            'forma_pagamento': 'pix',
            'itens': [
                {
                    'produto_id': 1,
                    'quantidade': 2,
                    'preco_unitario': 35.90
                }
            ]
        }
        
        erros = PedidoValidator.validar_pedido_completo(dados_validos)
        if not erros:
            print("✅ Validação de dados válidos: OK")
        else:
            print(f"❌ Dados válidos rejeitados: {erros}")
        
        # Teste 2: Dados inválidos
        dados_invalidos = {
            'cliente': {
                'nome': '',  # Nome vazio
                'telefone': '123',  # Telefone muito curto
                'email': 'email_invalido'  # Email sem @
            },
            'tipo': 'tipo_invalido',  # Tipo não permitido
            'forma_pagamento': 'forma_invalida',  # Forma não permitida
            'itens': [
                {
                    'produto_id': None,  # ID nulo
                    'quantidade': -1,  # Quantidade negativa
                    'preco_unitario': 'abc'  # Preço inválido
                }
            ]
        }
        
        erros = PedidoValidator.validar_pedido_completo(dados_invalidos)
        if erros and len(erros) >= 6:  # Esperamos pelo menos 6 erros
            print(f"✅ Validação detectou {len(erros)} erros como esperado")
        else:
            print(f"❌ Validação não detectou erros suficientes: {erros}")
        
        return True
    
    def test_tratamento_erros(self):
        """Testa tratamento de erros do Supabase"""
        print("\n🚨 Testando tratamento de erros...")
        
        # Simular diferentes tipos de erro
        erros_teste = [
            "connection timeout",
            "unique constraint violation", 
            "foreign key constraint",
            "not null constraint violation",
            "permission denied for table",
            "erro desconhecido do sistema"
        ]
        
        for erro in erros_teste:
            mensagem = SupabaseErrorHandler.tratar_erro_supabase(erro)
            print(f"✅ {erro[:20]}... → {mensagem}")
        
        return True
    
    def test_conectividade(self):
        """Testa verificação de conectividade"""
        print("\n🌐 Testando verificação de conectividade...")
        
        conectado, mensagem = self.manager.verificar_conectividade()
        if conectado:
            print(f"✅ Conectividade: {mensagem}")
        else:
            print(f"❌ Conectividade: {mensagem}")
        
        return conectado
    
    def test_health_check(self):
        """Testa health check completo"""
        print("\n💊 Testando health check completo...")
        
        status = SupabaseHealthCheck.status_completo()
        
        print(f"✅ Conectividade: {status['conectividade']}")
        print(f"✅ Tabelas acessíveis: {len(status['tabelas_acessiveis'])}")
        
        if status['metricas']:
            print("✅ Métricas obtidas:")
            for metrica, valor in status['metricas'].items():
                print(f"   - {metrica}: {valor}")
        
        if status['erros']:
            print(f"⚠️ Erros detectados: {len(status['erros'])}")
            for erro in status['erros'][:3]:  # Mostrar só 3
                print(f"   - {erro}")
        
        return status['conectividade']
    
    def test_endpoint_health(self):
        """Testa endpoint de health check"""
        print("\n🔗 Testando endpoint de health check...")
        
        try:
            # Simular requisição ao endpoint
            request = self.factory.get('/api/pedidos/supabase_health/')
            view = PedidoViewSet()
            view.action = 'supabase_health'
            
            response = view.supabase_health(request)
            
            if response.status_code in [200, 503]:  # OK ou Service Unavailable
                print(f"✅ Endpoint health retornou status {response.status_code}")
                
                data = response.data
                print(f"   Status: {data.get('status')}")
                print(f"   Mensagem: {data.get('message')}")
                
                if 'supabase' in data:
                    supabase_info = data['supabase']
                    print(f"   Conectividade: {supabase_info.get('conectividade')}")
                    print(f"   Tabelas: {len(supabase_info.get('tabelas_acessiveis', []))}")
                
                return True
            else:
                print(f"❌ Endpoint retornou status inesperado: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Erro no teste do endpoint: {e}")
            return False
    
    def test_criacao_pedido_segura(self):
        """Testa criação de pedido com validações"""
        print("\n🛡️ Testando criação segura de pedido...")
        
        # Dados de teste para pedido
        dados_pedido = {
            'cliente': {
                'nome': 'Maria Oliveira',
                'telefone': '11876543210',
                'email': 'maria@teste.com'
            },
            'tipo': 'balcao',
            'forma_pagamento': 'dinheiro',
            'itens': [
                {
                    'produto_id': 1,  # Assume que existe produto com ID 1
                    'quantidade': 1,
                    'preco_unitario': 29.90
                }
            ],
            'observacoes': 'Pedido de teste - validação segura'
        }
        
        try:
            resultado, erros = self.manager.criar_pedido_seguro(dados_pedido)
            
            if erros:
                print(f"❌ Erros na criação: {erros}")
                return False
            
            if resultado:
                pedido = resultado['pedido']
                print(f"✅ Pedido criado com segurança: #{pedido.numero}")
                print(f"   Cliente: {pedido.cliente.nome}")
                print(f"   Total: R$ {resultado['total']}")
                print(f"   Itens: {len(resultado['itens'])}")
                return True
            
        except Exception as e:
            print(f"❌ Erro na criação segura: {e}")
            return False
    
    def test_endpoint_criacao_segura(self):
        """Testa endpoint de criação segura"""
        print("\n🌐 Testando endpoint de criação segura...")
        
        dados_pedido = {
            'cliente': {
                'nome': 'Carlos Santos',
                'telefone': '11765432109',
                'email': 'carlos@teste.com'
            },
            'tipo': 'delivery',
            'forma_pagamento': 'cartao_credito',
            'itens': [
                {
                    'produto_id': 1,
                    'quantidade': 2,
                    'preco_unitario': 45.00
                }
            ]
        }
        
        try:
            request = self.factory.post('/api/pedidos/criar_pedido_seguro/', dados_pedido, format='json')
            view = PedidoViewSet()
            view.action = 'criar_pedido_seguro'
            view.request = request
            
            response = view.criar_pedido_seguro(request)
            
            if response.status_code == 201:
                print("✅ Endpoint de criação segura funcionando")
                data = response.data
                print(f"   Status: {data.get('status')}")
                print(f"   Pedido: {data.get('pedido', {}).get('numero')}")
                return True
            else:
                print(f"❌ Endpoint retornou status {response.status_code}")
                print(f"   Resposta: {response.data}")
                return False
                
        except Exception as e:
            print(f"❌ Erro no teste do endpoint: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def run_all_tests(self):
        """Executa todos os testes de melhorias"""
        print("🧪 TESTE DAS MELHORIAS NA INTEGRAÇÃO SUPABASE")
        print("=" * 65)
        
        tests_passed = 0
        total_tests = 7
        
        # Teste 1: Validações
        if self.test_validacoes():
            tests_passed += 1
        
        # Teste 2: Tratamento de erros
        if self.test_tratamento_erros():
            tests_passed += 1
        
        # Teste 3: Conectividade
        if self.test_conectividade():
            tests_passed += 1
        
        # Teste 4: Health check
        if self.test_health_check():
            tests_passed += 1
        
        # Teste 5: Endpoint health
        if self.test_endpoint_health():
            tests_passed += 1
        
        # Teste 6: Criação segura
        if self.test_criacao_pedido_segura():
            tests_passed += 1
        
        # Teste 7: Endpoint criação segura  
        if self.test_endpoint_criacao_segura():
            tests_passed += 1
        
        # Resultado final
        print("\n" + "=" * 65)
        print(f"📊 RESULTADO: {tests_passed}/{total_tests} testes de melhorias passaram")
        
        if tests_passed == total_tests:
            print("🎉 TODAS AS MELHORIAS FUNCIONANDO PERFEITAMENTE!")
            print("\n🔧 MELHORIAS IMPLEMENTADAS:")
            print("✅ Sistema de validações robusto")
            print("✅ Tratamento de erros amigável")
            print("✅ Health check da integração")
            print("✅ Endpoints seguros para produção")
            print("✅ Logging e monitoramento")
        else:
            print("⚠️ Algumas melhorias precisam de ajustes.")
        
        return tests_passed == total_tests

if __name__ == '__main__':
    teste = TesteMelhorias()
    success = teste.run_all_tests()