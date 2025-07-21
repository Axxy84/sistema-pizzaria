#!/usr/bin/env python
"""
Script para adicionar a terceira parte das pizzas fornecidas pelo usuário
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoProject.settings')
django.setup()

from apps.produtos.models import Produto, Categoria, ProdutoPreco, Tamanho
from decimal import Decimal

def adicionar_pizzas_parte3():
    """Adicionar terceira lista de pizzas"""
    
    # Obter categorias
    categoria_salgadas = Categoria.objects.get(nome='Pizzas Salgadas')
    categoria_especiais = Categoria.objects.get(nome='Pizzas Especiais')
    
    # Obter tamanhos
    tamanhos = {
        'pequena': Tamanho.objects.get(nome='Pequena'),
        'media': Tamanho.objects.get(nome='Média'),
        'grande': Tamanho.objects.get(nome='Grande'),
        'familia': Tamanho.objects.get(nome='Família'),
    }
    
    # Terceira lista de pizzas do usuário
    pizzas_parte3 = [
        {
            'nome': 'Pizza Lasanha',
            'categoria': categoria_especiais,
            'ingredientes': 'Molho, mussarela, presunto, carne seca, tomate e orégano',
            'descricao': 'Sabor tradicional da lasanha em formato pizza',
            'precos': {'pequena': 37.00, 'media': 42.00, 'grande': 47.00, 'familia': 55.00}
        },
        {
            'nome': 'Pizza Lombo Canadense',
            'categoria': categoria_salgadas,
            'ingredientes': 'Molho, mussarela, presunto, lombo canadense e orégano',
            'descricao': 'Lombo canadense premium com presunto selecionado',
            'precos': {'pequena': 32.00, 'media': 38.00, 'grande': 47.00, 'familia': 55.00}
        },
        {
            'nome': 'Pizza Lombo Canadense ao Catupiry',
            'categoria': categoria_especiais,
            'ingredientes': 'Molho, mussarela, presunto, lombo canadense, catupiry e orégano',
            'descricao': 'Lombo canadense com cremoso catupiry',
            'precos': {'pequena': 35.00, 'media': 41.00, 'grande': 50.00, 'familia': 58.00}
        },
        {
            'nome': 'Pizza Lombo Canadense com Cheddar',
            'categoria': categoria_especiais,
            'ingredientes': 'Molho, mussarela, lombo canadense, cheddar e orégano',
            'descricao': 'Lombo canadense com sabor intenso do cheddar',
            'precos': {'pequena': 36.00, 'media': 42.00, 'grande': 51.00, 'familia': 59.00}
        },
        {
            'nome': 'Pizza Luzitana',
            'categoria': categoria_salgadas,
            'ingredientes': 'Molho, mussarela, ervilha, ovo, cebola e orégano',
            'descricao': 'Tradicional receita portuguesa com ovos e ervilha',
            'precos': {'pequena': 33.00, 'media': 37.00, 'grande': 44.00, 'familia': 52.00}
        },
        {
            'nome': 'Pizza Milho Verde ao Catupiry',
            'categoria': categoria_salgadas,
            'ingredientes': 'Molho, mussarela, milho verde, catupiry, e orégano',
            'descricao': 'Doçura do milho verde com cremosidade do catupiry',
            'precos': {'pequena': 33.00, 'media': 38.00, 'grande': 40.00, 'familia': 48.00}
        },
        {
            'nome': 'Pizza Mineira',
            'categoria': categoria_especiais,
            'ingredientes': 'Molho, mussarela, lombo canadense, milho, bacon, catupiry e orégano',
            'descricao': 'Sabores típicos de Minas Gerais em uma pizza',
            'precos': {'pequena': 35.00, 'media': 39.00, 'grande': 45.00, 'familia': 52.00}
        },
        {
            'nome': 'Pizza Moda da Casa',
            'categoria': categoria_especiais,
            'ingredientes': 'Molho, mussarela, carne seca, vinagrete, banana da terra, provolone, bacon e orégano',
            'descricao': 'Nossa especialidade exclusiva com ingredientes únicos',
            'precos': {'pequena': 35.00, 'media': 43.00, 'grande': 50.00, 'familia': 57.00}
        },
        {
            'nome': 'Pizza Moda do Pizzaiolo',
            'categoria': categoria_especiais,
            'ingredientes': 'Molho, mussarela, frango desfiado, cheddar, bacon, banana da terra, milho verde e orégano',
            'descricao': 'Criação especial do nosso pizzaiolo com ingredientes selecionados',
            'precos': {'pequena': 38.00, 'media': 45.00, 'grande': 51.00, 'familia': 58.00}
        },
        {
            'nome': 'Pizza Palharina',
            'categoria': categoria_salgadas,
            'ingredientes': 'Molho, mussarela, milho, azeitona sem caroço, batata palha e orégano',
            'descricao': 'Crocância da batata palha com sabor especial',
            'precos': {'pequena': 29.00, 'media': 37.00, 'grande': 43.00, 'familia': 49.00}
        },
        {
            'nome': 'Pizza Palharina sem Milho',
            'categoria': categoria_salgadas,
            'ingredientes': 'Molho, mussarela, batata palha, azeitona sem caroço e orégano',
            'descricao': 'Versão clássica da palharina sem milho',
            'precos': {'pequena': 30.00, 'media': 39.00, 'grande': 45.00, 'familia': 52.00}
        }
    ]
    
    # Pizzas que precisam ser atualizadas (já existem)
    pizzas_atualizar = [
        {
            'nome': 'Pizza Marguerita',
            'ingredientes': 'Molho, mussarela, tomate, manjericão e orégano',
            'descricao': 'Clássica pizza italiana com sabores frescos',
            'precos': {'pequena': 28.00, 'media': 35.00, 'grande': 42.00, 'familia': 49.00}
        },
        {
            'nome': 'Pizza Milho Verde',
            'ingredientes': 'Molho, mussarela, milho verde e orégano',
            'descricao': 'Doçura natural do milho verde selecionado',
            'precos': {'pequena': 30.00, 'media': 35.00, 'grande': 37.00, 'familia': 45.00}
        },
        {
            'nome': 'Pizza Mussarela',
            'ingredientes': 'Molho, mussarela, tomate em rodela e orégano',
            'descricao': 'Simplicidade e sabor com mussarela de primeira qualidade',
            'precos': {'pequena': 28.00, 'media': 35.00, 'grande': 41.00, 'familia': 48.00}
        }
    ]
    
    def criar_pizza(pizza_data):
        """Criar nova pizza"""
        try:
            # Verificar se já existe
            if Produto.objects.filter(nome=pizza_data['nome']).exists():
                print(f"❌ Pizza '{pizza_data['nome']}' já existe - pulando")
                return False
            
            # Criar produto
            pizza = Produto.objects.create(
                nome=pizza_data['nome'],
                categoria=pizza_data['categoria'],
                tipo_produto='pizza',
                descricao=pizza_data['descricao'],
                ingredientes=pizza_data['ingredientes'],
                ativo=True
            )
            
            print(f"✅ Pizza '{pizza.nome}' criada!")
            
            # Criar preços por tamanho
            for tamanho_nome, preco in pizza_data['precos'].items():
                if tamanho_nome in tamanhos:
                    ProdutoPreco.objects.create(
                        produto=pizza,
                        tamanho=tamanhos[tamanho_nome],
                        preco=Decimal(str(preco))
                    )
                    print(f"   - {tamanhos[tamanho_nome].nome}: R$ {preco:.2f}")
            
            return True
            
        except Exception as e:
            print(f"❌ Erro ao criar pizza '{pizza_data['nome']}': {e}")
            return False
    
    def atualizar_pizza(pizza_data):
        """Atualizar pizza existente"""
        try:
            pizza = Produto.objects.get(nome=pizza_data['nome'])
            
            # Atualizar campos
            pizza.ingredientes = pizza_data['ingredientes']
            pizza.descricao = pizza_data['descricao']
            pizza.save()
            
            print(f"🔄 Pizza '{pizza.nome}' atualizada!")
            
            # Atualizar preços
            pizza.precos.all().delete()
            
            for tamanho_nome, preco in pizza_data['precos'].items():
                if tamanho_nome in tamanhos:
                    ProdutoPreco.objects.create(
                        produto=pizza,
                        tamanho=tamanhos[tamanho_nome],
                        preco=Decimal(str(preco))
                    )
                    print(f"   - {tamanhos[tamanho_nome].nome}: R$ {preco:.2f}")
            
            return True
            
        except Produto.DoesNotExist:
            print(f"❌ Pizza '{pizza_data['nome']}' não encontrada")
            return False
    
    print("🍕 ADICIONANDO TERCEIRA PARTE DAS PIZZAS 🍕")
    print("=" * 50)
    
    pizzas_criadas = 0
    pizzas_atualizadas = 0
    pizzas_erros = 0
    
    # Atualizar pizzas existentes primeiro
    print("\n🔄 ATUALIZANDO PIZZAS EXISTENTES:")
    for pizza_data in pizzas_atualizar:
        print(f"\n📝 Atualizando: {pizza_data['nome']}")
        
        if atualizar_pizza(pizza_data):
            pizzas_atualizadas += 1
        else:
            pizzas_erros += 1
    
    # Processar novas pizzas
    print("\n✅ CRIANDO NOVAS PIZZAS:")
    for pizza_data in pizzas_parte3:
        print(f"\n📝 Processando: {pizza_data['nome']}")
        
        if criar_pizza(pizza_data):
            pizzas_criadas += 1
        else:
            pizzas_erros += 1
    
    # Estatísticas finais
    print("\n" + "=" * 50)
    print("📊 RELATÓRIO FINAL - PARTE 3")
    print("=" * 50)
    
    total_pizzas = Produto.objects.filter(tipo_produto='pizza').exclude(nome__icontains='PROMOCIONAL').count()
    total_promocionais = Produto.objects.filter(nome__icontains='PROMOCIONAL').count()
    
    print(f"🔄 Pizzas atualizadas: {pizzas_atualizadas}")
    print(f"✅ Pizzas criadas: {pizzas_criadas}")
    print(f"❌ Erros: {pizzas_erros}")
    print(f"🍕 Total de pizzas regulares: {total_pizzas}")
    print(f"🔥 Total de pizzas promocionais: {total_promocionais}")
    print(f"📊 Total geral: {total_pizzas + total_promocionais}")
    
    # Contagem por categoria
    print("\n📋 Distribuição por categoria:")
    for categoria in [categoria_salgadas, categoria_especiais]:
        count = Produto.objects.filter(categoria=categoria, tipo_produto='pizza').exclude(nome__icontains='PROMOCIONAL').count()
        print(f"   - {categoria.nome}: {count} pizzas")
    
    # Outras categorias
    outras_categorias = Categoria.objects.exclude(nome__in=['Pizzas Salgadas', 'Pizzas Especiais'])
    for categoria in outras_categorias:
        count = Produto.objects.filter(categoria=categoria, tipo_produto='pizza').exclude(nome__icontains='PROMOCIONAL').count()
        if count > 0:
            print(f"   - {categoria.nome}: {count} pizzas")
    
    print("\n🎉 TERCEIRA PARTE CONCLUÍDA COM SUCESSO! 🎉")

if __name__ == '__main__':
    adicionar_pizzas_parte3()