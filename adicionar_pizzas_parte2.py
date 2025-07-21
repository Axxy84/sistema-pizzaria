#!/usr/bin/env python
"""
Script para adicionar a segunda parte das pizzas fornecidas pelo usuário
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoProject.settings')
django.setup()

from apps.produtos.models import Produto, Categoria, ProdutoPreco, Tamanho
from decimal import Decimal

def adicionar_pizzas_parte2():
    """Adicionar segunda lista de pizzas"""
    
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
    
    # Segunda lista de pizzas do usuário
    pizzas_parte2 = [
        {
            'nome': 'Pizza Carne do Sol',
            'categoria': categoria_especiais,
            'ingredientes': 'Molho, mussarela, carne desfiada, vinagrete e orégano',
            'descricao': 'Deliciosa carne do sol desfiada com vinagrete especial',
            'precos': {'pequena': 36.00, 'media': 39.00, 'grande': 49.00, 'familia': 55.00}
        },
        {
            'nome': 'Pizza Carne do Sol ao Catupiry',
            'categoria': categoria_especiais,
            'ingredientes': 'Molho, mussarela, carne desfiada, vinagrete, catupiry e orégano',
            'descricao': 'Carne do sol com cremoso catupiry e vinagrete',
            'precos': {'pequena': 38.00, 'media': 42.00, 'grande': 52.00, 'familia': 58.00}
        },
        {
            'nome': 'Pizza Cheddar Especial',
            'categoria': categoria_especiais,
            'ingredientes': 'Molho, mussarela, cheddar, parmesão, gorgonzola e orégano',
            'descricao': 'Combinação especial de três queijos nobres',
            'precos': {'pequena': 36.00, 'media': 44.00, 'grande': 49.00, 'familia': 58.00}
        },
        {
            'nome': 'Pizza Defumados',
            'categoria': categoria_especiais,
            'ingredientes': 'Molho, mussarela, provolone, lombo canadense, calabresa, bacon, cebola e orégano',
            'descricao': 'Seleção de carnes defumadas premium',
            'precos': {'pequena': 37.00, 'media': 43.00, 'grande': 50.00, 'familia': 57.00}
        },
        {
            'nome': 'Pizza Especial',
            'categoria': categoria_especiais,
            'ingredientes': 'Molho, mussarela, frango desfiado, palmito, milho, catupiry, milho verde e orégano',
            'descricao': 'Nossa pizza especial da casa com ingredientes selecionados',
            'precos': {'pequena': 33.00, 'media': 38.00, 'grande': 45.00, 'familia': 50.00}
        },
        {
            'nome': 'Pizza Frango',
            'categoria': categoria_salgadas,
            'ingredientes': 'Molho, mussarela, frango desfiado, tomate em rodela e orégano',
            'descricao': 'Frango desfiado temperado com tomates frescos',
            'precos': {'pequena': 28.00, 'media': 37.00, 'grande': 45.00, 'familia': 49.00}
        },
        {
            'nome': 'Pizza Frango com Palmito',
            'categoria': categoria_salgadas,
            'ingredientes': 'Molho, mussarela, frango, catupiry, bacon e orégano',
            'descricao': 'Frango com palmito, catupiry e bacon',
            'precos': {'pequena': 34.00, 'media': 39.00, 'grande': 48.00, 'familia': 52.00}
        },
        {
            'nome': 'Pizza Frango com Milho',
            'categoria': categoria_salgadas,
            'ingredientes': 'Molho, mussarela, frango desfiado, milho verde e orégano',
            'descricao': 'Combinação clássica de frango com milho doce',
            'precos': {'pequena': 29.00, 'media': 38.00, 'grande': 46.00, 'familia': 50.00}
        },
        {
            'nome': 'Pizza Frango com Brócolis',
            'categoria': categoria_salgadas,
            'ingredientes': 'Molho, mussarela, frango desfiado, palmito, brócolis e orégano',
            'descricao': 'Opção saudável com frango, brócolis e palmito',
            'precos': {'pequena': 34.00, 'media': 38.00, 'grande': 45.00, 'familia': 52.00}
        },
        {
            'nome': 'Pizza Frango com Cheddar',
            'categoria': categoria_salgadas,
            'ingredientes': 'Molho, mussarela, frango desfiado, cheddar, cebola e orégano',
            'descricao': 'Frango com sabor intenso do cheddar',
            'precos': {'pequena': 37.00, 'media': 42.00, 'grande': 48.00, 'familia': 55.00}
        },
        {
            'nome': 'Pizza Frango com Bacon',
            'categoria': categoria_salgadas,
            'ingredientes': 'Molho, mussarela, frango, bacon e orégano',
            'descricao': 'Combinação irresistível de frango com bacon crocante',
            'precos': {'pequena': 35.00, 'media': 40.00, 'grande': 47.00, 'familia': 55.00}
        },
        {
            'nome': 'Pizza Gorgonzola',
            'categoria': categoria_especiais,
            'ingredientes': 'Molho, mussarela, gorgonzola e orégano',
            'descricao': 'Para apreciadores do sabor marcante do gorgonzola',
            'precos': {'pequena': 35.00, 'media': 38.00, 'grande': 43.00, 'familia': 52.00}
        },
        {
            'nome': 'Pizza Hot Dog',
            'categoria': categoria_salgadas,
            'ingredientes': 'Molho, mussarela, salsicha, batata palha e orégano',
            'descricao': 'Sabor nostálgico do hot dog em formato pizza',
            'precos': {'pequena': 32.00, 'media': 37.00, 'grande': 42.00, 'familia': 47.00}
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
    
    def atualizar_frango_catupiry():
        """Atualizar pizza Frango ao Catupiry existente"""
        try:
            pizza = Produto.objects.get(nome='Pizza Frango ao Catupiry')
            
            # Atualizar campos
            pizza.ingredientes = 'Molho, mussarela, frango desfiado, catupiry e orégano'
            pizza.descricao = 'Frango temperado com o cremoso catupiry original'
            pizza.save()
            
            print(f"🔄 Pizza '{pizza.nome}' atualizada!")
            
            # Atualizar preços
            pizza.precos.all().delete()
            
            novos_precos = {'pequena': 30.00, 'media': 36.00, 'grande': 45.00, 'familia': 53.00}
            for tamanho_nome, preco in novos_precos.items():
                if tamanho_nome in tamanhos:
                    ProdutoPreco.objects.create(
                        produto=pizza,
                        tamanho=tamanhos[tamanho_nome],
                        preco=Decimal(str(preco))
                    )
                    print(f"   - {tamanhos[tamanho_nome].nome}: R$ {preco:.2f}")
            
            return True
            
        except Produto.DoesNotExist:
            print(f"❌ Pizza 'Pizza Frango ao Catupiry' não encontrada")
            return False
    
    print("🍕 ADICIONANDO SEGUNDA PARTE DAS PIZZAS 🍕")
    print("=" * 50)
    
    pizzas_criadas = 0
    pizzas_atualizadas = 0
    pizzas_erros = 0
    
    # Atualizar Frango ao Catupiry primeiro
    print(f"\n📝 Atualizando: Pizza Frango ao Catupiry")
    if atualizar_frango_catupiry():
        pizzas_atualizadas += 1
    else:
        pizzas_erros += 1
    
    # Processar novas pizzas
    for pizza_data in pizzas_parte2:
        print(f"\n📝 Processando: {pizza_data['nome']}")
        
        if criar_pizza(pizza_data):
            pizzas_criadas += 1
        else:
            pizzas_erros += 1
    
    # Estatísticas finais
    print("\n" + "=" * 50)
    print("📊 RELATÓRIO FINAL - PARTE 2")
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
    
    print("\n🎉 SEGUNDA PARTE CONCLUÍDA COM SUCESSO! 🎉")

if __name__ == '__main__':
    adicionar_pizzas_parte2()