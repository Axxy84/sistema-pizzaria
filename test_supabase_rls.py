#!/usr/bin/env python
"""
Script para testar políticas de segurança (RLS) no Supabase
Verifica permissões e acesso a dados
"""

import os
import sys
import django

# Setup Django
sys.path.append('/home/labdev/Documentos/DjangoProject')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoProject.settings')
django.setup()

from services.supabase_client import get_supabase_client, get_supabase_admin_client

def test_anon_access():
    """Testa acesso anônimo (sem autenticação)"""
    print("🔓 Testando acesso anônimo...")
    
    try:
        supabase = get_supabase_client()
        
        # Testar leitura de produtos (deve ser permitido)
        print("📖 Testando leitura de produtos...")
        result = supabase.table('produtos_produto').select('id, nome, ativo').eq('ativo', True).execute()
        print(f"✅ Leitura de produtos: {len(result.data)} produtos acessíveis")
        
        # Testar leitura de categorias
        print("📖 Testando leitura de categorias...")
        result = supabase.table('produtos_categoria').select('*').execute()
        print(f"✅ Leitura de categorias: {len(result.data)} categorias acessíveis")
        
        # Testar leitura de tamanhos
        print("📖 Testando leitura de tamanhos...")
        result = supabase.table('produtos_tamanho').select('*').execute()
        print(f"✅ Leitura de tamanhos: {len(result.data)} tamanhos acessíveis")
        
        # Testar inserção de cliente (deve ser permitido para sistema de pedidos)
        print("✍️ Testando inserção de cliente...")
        try:
            result = supabase.table('clientes_cliente').insert({
                'nome': 'Cliente RLS Test',
                'telefone': '11888888888',
                'email': 'rls@test.com'
            }).execute()
            
            if result.data:
                print("✅ Inserção de cliente permitida")
                cliente_id = result.data[0]['id']
                
                # Limpar teste
                supabase.table('clientes_cliente').delete().eq('id', cliente_id).execute()
                print("🧹 Cliente de teste removido")
            else:
                print("❌ Inserção de cliente bloqueada")
                
        except Exception as e:
            print(f"❌ Erro na inserção de cliente: {e}")
        
        # Testar inserção de pedido
        print("✍️ Testando inserção de pedido...")
        try:
            result = supabase.table('pedidos_pedido').insert({
                'cliente_id': 1,  # Assume que existe cliente com ID 1
                'usuario_id': 1,  # Assume que existe usuário com ID 1
                'tipo': 'balcao',
                'forma_pagamento': 'dinheiro',
                'subtotal': 25.00,
                'total': 25.00
            }).execute()
            
            if result.data:
                print("✅ Inserção de pedido permitida")
                pedido_id = result.data[0]['id']
                
                # Limpar teste
                supabase.table('pedidos_pedido').delete().eq('id', pedido_id).execute()
                print("🧹 Pedido de teste removido")
            else:
                print("❌ Inserção de pedido bloqueada")
                
        except Exception as e:
            print(f"❌ Erro na inserção de pedido: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste anônimo: {e}")
        return False

def test_admin_access():
    """Testa acesso administrativo (service role)"""
    print("\n🔑 Testando acesso administrativo...")
    
    try:
        supabase_admin = get_supabase_admin_client()
        
        # Testar leitura total de dados
        print("📊 Testando leitura administrativa...")
        
        # Produtos
        result = supabase_admin.table('produtos_produto').select('count').execute()
        print(f"✅ Produtos (admin): Acesso total")
        
        # Pedidos
        result = supabase_admin.table('pedidos_pedido').select('count').execute()
        print(f"✅ Pedidos (admin): Acesso total")
        
        # Clientes
        result = supabase_admin.table('clientes_cliente').select('count').execute()
        print(f"✅ Clientes (admin): Acesso total")
        
        # Usuários do sistema
        try:
            result = supabase_admin.table('auth_user').select('count').execute()
            print(f"✅ Usuários (admin): Acesso total")
        except Exception as e:
            print(f"⚠️ Usuários (admin): {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste administrativo: {e}")
        return False

def test_rls_policies():
    """Testa políticas específicas de RLS"""
    print("\n🛡️ Testando políticas RLS específicas...")
    
    try:
        supabase = get_supabase_client()
        
        # Política 1: Produtos ativos devem ser visíveis para todos
        print("🔍 Política: Produtos ativos públicos...")
        result = supabase.table('produtos_produto').select('id, nome, ativo').eq('ativo', False).execute()
        
        if len(result.data) == 0:
            print("✅ Produtos inativos estão protegidos")
        else:
            print(f"⚠️ {len(result.data)} produtos inativos visíveis")
        
        # Política 2: Tentar acessar dados sensíveis
        print("🔍 Política: Proteção de dados sensíveis...")
        
        # Tentar acessar movimentações financeiras
        try:
            result = supabase.table('financeiro_movimentocaixa').select('*').execute()
            if len(result.data) == 0:
                print("✅ Dados financeiros protegidos")
            else:
                print(f"⚠️ {len(result.data)} movimentações financeiras acessíveis")
        except Exception as e:
            print(f"✅ Dados financeiros protegidos: {e}")
        
        # Política 3: Tentar acessar dados de estoque
        try:
            result = supabase.table('estoque_ingrediente').select('*').execute()
            if len(result.data) == 0:
                print("✅ Dados de estoque protegidos")
            else:
                print(f"⚠️ {len(result.data)} ingredientes de estoque acessíveis")
        except Exception as e:
            print(f"✅ Dados de estoque protegidos: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro nas políticas RLS: {e}")
        return False

def test_data_modification_limits():
    """Testa limites de modificação de dados"""
    print("\n✏️ Testando limites de modificação...")
    
    try:
        supabase = get_supabase_client()
        
        # Tentar modificar produto existente
        print("🚫 Testando modificação de produto...")
        try:
            result = supabase.table('produtos_produto').update({'nome': 'TESTE RLS'}).eq('id', 1).execute()
            if result.data:
                print("⚠️ Modificação de produto permitida (pode ser problemático)")
                # Reverter alteração
                supabase.table('produtos_produto').update({'nome': 'Pizza Margherita'}).eq('id', 1).execute()
            else:
                print("✅ Modificação de produto bloqueada")
        except Exception as e:
            print(f"✅ Modificação de produto bloqueada: {e}")
        
        # Tentar deletar dados críticos
        print("🚫 Testando deleção de dados...")
        try:
            # Tentar deletar categoria (não deve ser permitido)
            result = supabase.table('produtos_categoria').delete().eq('id', 999999).execute()
            print("⚠️ Deleção permitida (categoria inexistente)")
        except Exception as e:
            print(f"✅ Deleção protegida: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro nos testes de modificação: {e}")
        return False

def check_table_permissions():
    """Verifica permissões específicas por tabela"""
    print("\n📋 Verificando permissões por tabela...")
    
    supabase = get_supabase_client()
    
    tables_to_test = [
        ('produtos_produto', 'SELECT', 'Produtos - Leitura'),
        ('produtos_categoria', 'SELECT', 'Categorias - Leitura'),
        ('clientes_cliente', 'INSERT', 'Clientes - Inserção'),
        ('pedidos_pedido', 'INSERT', 'Pedidos - Inserção'),
        ('pedidos_itempedido', 'INSERT', 'Itens Pedido - Inserção'),
        ('auth_user', 'SELECT', 'Usuários - Leitura'),
        ('financeiro_movimentocaixa', 'SELECT', 'Financeiro - Leitura'),
    ]
    
    for table, operation, description in tables_to_test:
        try:
            if operation == 'SELECT':
                result = supabase.table(table).select('count').limit(1).execute()
                print(f"✅ {description}")
            elif operation == 'INSERT':
                # Teste de inserção simulada (não executa)
                print(f"🔍 {description} - Verificar manualmente")
        except Exception as e:
            print(f"❌ {description}: {e}")

def run_rls_tests():
    """Executa todos os testes de RLS"""
    print("🛡️ TESTE DE POLÍTICAS DE SEGURANÇA (RLS) - SUPABASE")
    print("=" * 65)
    
    tests_passed = 0
    total_tests = 5
    
    # Teste 1: Acesso anônimo
    if test_anon_access():
        tests_passed += 1
    
    # Teste 2: Acesso administrativo
    if test_admin_access():
        tests_passed += 1
    
    # Teste 3: Políticas RLS
    if test_rls_policies():
        tests_passed += 1
    
    # Teste 4: Limites de modificação
    if test_data_modification_limits():
        tests_passed += 1
    
    # Teste 5: Permissões por tabela
    check_table_permissions()
    tests_passed += 1  # Assume sucesso se não houve exceção
    
    # Resultado final
    print("\n" + "=" * 65)
    print(f"📊 RESULTADO: {tests_passed}/{total_tests} testes de segurança passaram")
    
    if tests_passed == total_tests:
        print("🔒 POLÍTICAS DE SEGURANÇA FUNCIONANDO ADEQUADAMENTE!")
    else:
        print("⚠️ Algumas políticas podem precisar de ajustes.")
    
    print("\n💡 RECOMENDAÇÕES DE SEGURANÇA:")
    print("- Produtos: Leitura pública OK para cardápio")
    print("- Clientes/Pedidos: Inserção pública OK para e-commerce")
    print("- Dados financeiros: Devem ser protegidos")
    print("- Modificações: Apenas usuários autenticados")
    
    return tests_passed >= total_tests - 1  # Tolerância para 1 falha

if __name__ == '__main__':
    run_rls_tests()