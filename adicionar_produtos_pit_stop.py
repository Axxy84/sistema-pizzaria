#!/usr/bin/env python
"""
Script para adicionar produtos da Pit Stop Pizzaria no Supabase
"""
import os
import django
import sys
from decimal import Decimal

# Configurar Django
sys.path.append('/home/labdev/Documentos/DjangoProject')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoProject.settings')
django.setup()

from apps.produtos.models import Produto, Categoria

def limpar_produtos_existentes():
    """Remove produtos existentes para evitar duplicatas"""
    print("🧹 Limpando produtos existentes...")
    count = Produto.objects.all().delete()[0]
    print(f"   ✅ {count} produtos removidos")

def criar_categorias():
    """Cria as categorias necessárias"""
    print("📁 Criando categorias...")
    
    categorias = [
        {'nome': 'Pizzas Salgadas', 'descricao': 'Pizzas tradicionais e especiais'},
        {'nome': 'Pizzas Doces', 'descricao': 'Pizzas com sabores doces'},
        {'nome': 'Bordas Recheadas', 'descricao': 'Opções de borda para pizzas'},
    ]
    
    cats_criadas = {}
    for cat_data in categorias:
        categoria, criada = Categoria.objects.get_or_create(
            nome=cat_data['nome'],
            defaults={'descricao': cat_data['descricao']}
        )
        cats_criadas[cat_data['nome']] = categoria
        status = "✅ Criada" if criada else "♻️  Já existe"
        print(f"   {status}: {categoria.nome}")
    
    return cats_criadas

def adicionar_pizzas_salgadas(categoria):
    """Adiciona pizzas salgadas"""
    print("🍕 Adicionando pizzas salgadas...")
    
    pizzas = [
        {
            'nome': 'Pizza Alho Frito',
            'descricao': 'Molho, mussarela, alho frito e orégano - 8 pedaços',
            'preco': Decimal('40.00')
        },
        {
            'nome': 'Pizza Atum',
            'descricao': 'Molho, mussarela, atum, cebola e orégano',
            'preco': Decimal('40.00')
        },
        {
            'nome': 'Pizza Bacon',
            'descricao': 'Molho, mussarela, bacon e orégano',
            'preco': Decimal('40.00')
        },
        {
            'nome': 'Pizza Baiana',
            'descricao': 'Molho, mussarela, calabresa moída, pimenta calabresa, tomate em rodela e orégano',
            'preco': Decimal('40.00')
        },
        {
            'nome': 'Pizza Baurú',
            'descricao': 'Molho, mussarela, presunto, milho verde e orégano',
            'preco': Decimal('40.00')
        },
        {
            'nome': 'Pizza Calabresa',
            'descricao': 'Molho, mussarela, calabresa, cebola e orégano',
            'preco': Decimal('40.00')
        },
        {
            'nome': 'Pizza Frango ao Catupiry',
            'descricao': 'Molho, mussarela, peito de frango e orégano',
            'preco': Decimal('40.00')
        },
        {
            'nome': 'Pizza Marguerita',
            'descricao': 'Molho, mussarela, tomate, manjericão e orégano',
            'preco': Decimal('40.00')
        },
        {
            'nome': 'Pizza Luzitana',
            'descricao': 'Molho, mussarela, ervilha, ovo, cebola e orégano',
            'preco': Decimal('40.00')
        },
        {
            'nome': 'Pizza Milho Verde',
            'descricao': 'Molho, mussarela, milho verde e orégano',
            'preco': Decimal('40.00')
        },
        {
            'nome': 'Pizza Mussarela',
            'descricao': 'Molho, mussarela, tomate em rodela e orégano',
            'preco': Decimal('40.00')
        },
        {
            'nome': 'Pizza Portuguesa sem Palmito',
            'descricao': 'Molho, mussarela, presunto, cebola, vinagrete, milho verde, ovos, pimentão e orégano',
            'preco': Decimal('40.00')
        },
        {
            'nome': 'Pizza Lombo',
            'descricao': 'Molho, mussarela, presunto, lombo canadense e orégano',
            'preco': Decimal('40.00')
        },
    ]
    
    for pizza_data in pizzas:
        produto, criado = Produto.objects.get_or_create(
            nome=pizza_data['nome'],
            defaults={
                'descricao': pizza_data['descricao'],
                'preco_unitario': pizza_data['preco'],
                'tipo_produto': 'pizza',
                'categoria': categoria,
                'ativo': True
            }
        )
        status = "✅ Criada" if criado else "♻️  Já existe"
        print(f"   {status}: {produto.nome} - R$ {produto.preco_unitario}")

def adicionar_pizzas_doces(categoria):
    """Adiciona pizzas doces"""
    print("🍰 Adicionando pizzas doces...")
    
    pizzas_doces = [
        {
            'nome': 'Pizza Banana Caramelizada',
            'descricao': 'Leite condensado, banana caramelizada e canela em pó',
            'preco': Decimal('40.00')
        },
        {
            'nome': 'Pizza Abacaxi Gratinado',
            'descricao': 'Leite condensado, mussarela, abacaxi gratinado e canela em pó',
            'preco': Decimal('40.00')
        },
        {
            'nome': 'Pizza Romeu e Julieta',
            'descricao': 'Leite condensado, mussarela e goiabada',
            'preco': Decimal('40.00')
        },
    ]
    
    for pizza_data in pizzas_doces:
        produto, criado = Produto.objects.get_or_create(
            nome=pizza_data['nome'],
            defaults={
                'descricao': pizza_data['descricao'],
                'preco_unitario': pizza_data['preco'],
                'tipo_produto': 'pizza',
                'categoria': categoria,
                'ativo': True
            }
        )
        status = "✅ Criada" if criado else "♻️  Já existe"
        print(f"   {status}: {produto.nome} - R$ {produto.preco_unitario}")

def adicionar_bordas_recheadas(categoria):
    """Adiciona opções de borda recheada"""
    print("🎂 Adicionando bordas recheadas...")
    
    bordas = [
        {'nome': 'Borda Catupiry', 'preco': Decimal('7.00')},
        {'nome': 'Borda Cheddar', 'preco': Decimal('8.00')},
        {'nome': 'Borda Mussarela', 'preco': Decimal('7.00')},
        {'nome': 'Borda Nutella', 'preco': Decimal('10.00')},
        {'nome': 'Borda Romeu e Julieta', 'preco': Decimal('10.00')},
        {'nome': 'Borda Beijinho', 'preco': Decimal('8.00')},
        {'nome': 'Borda Brigadeiro', 'preco': Decimal('8.00')},
        {'nome': 'Borda Doce de Leite', 'preco': Decimal('8.00')},
        {'nome': 'Borda Goiabada', 'preco': Decimal('7.00')},
    ]
    
    for borda_data in bordas:
        produto, criado = Produto.objects.get_or_create(
            nome=borda_data['nome'],
            defaults={
                'descricao': f'Borda recheada - Adicional para pizza',
                'preco_unitario': borda_data['preco'],
                'tipo_produto': 'borda',
                'categoria': categoria,
                'ativo': True
            }
        )
        status = "✅ Criada" if criado else "♻️  Já existe"
        print(f"   {status}: {produto.nome} - R$ {produto.preco_unitario}")

def main():
    """Função principal"""
    print("🍕 PIT STOP PIZZARIA - IMPORTAÇÃO DE PRODUTOS")
    print("=" * 50)
    
    try:
        # Limpar produtos existentes
        limpar_produtos_existentes()
        
        # Criar categorias
        categorias = criar_categorias()
        
        # Adicionar produtos
        adicionar_pizzas_salgadas(categorias['Pizzas Salgadas'])
        adicionar_pizzas_doces(categorias['Pizzas Doces'])
        adicionar_bordas_recheadas(categorias['Bordas Recheadas'])
        
        # Resumo final
        print("\n📊 RESUMO FINAL")
        print("=" * 30)
        for cat_nome, categoria in categorias.items():
            count = Produto.objects.filter(categoria=categoria).count()
            print(f"   {cat_nome}: {count} produtos")
        
        total = Produto.objects.count()
        print(f"\n🎉 TOTAL: {total} produtos adicionados com sucesso!")
        print("   Produtos disponíveis no frontend: http://127.0.0.1:8000/")
        
    except Exception as e:
        print(f"❌ ERRO: {e}")
        return False
    
    return True

if __name__ == "__main__":
    sucesso = main()
    if sucesso:
        print("\n✅ Importação concluída com sucesso!")
    else:
        print("\n❌ Falha na importação!")