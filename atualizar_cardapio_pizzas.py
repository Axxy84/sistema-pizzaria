#!/usr/bin/env python
"""
Script para atualizar e criar pizzas com base na lista fornecida pelo usuário
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoProject.settings')
django.setup()

from apps.produtos.models import Produto, Categoria, ProdutoPreco, Tamanho
from decimal import Decimal

def atualizar_cardapio_pizzas():
    """Atualizar cardápio com as novas pizzas fornecidas"""
    
    # Obter categorias
    categoria_salgadas = Categoria.objects.get(nome='Pizzas Salgadas')
    
    # Obter tamanhos
    tamanhos = {
        'pequena': Tamanho.objects.get(nome='Pequena'),
        'media': Tamanho.objects.get(nome='Média'),
        'grande': Tamanho.objects.get(nome='Grande'),
        'familia': Tamanho.objects.get(nome='Família'),
    }
    
    # Definir as novas pizzas do usuário
    pizzas_usuario = [
        {
            'nome': 'Pizza Bacon',
            'ingredientes': 'Molho, mussarela, bacon e orégano',
            'descricao': 'Pizza clássica com bacon crocante',
            'precos': {'pequena': 29.00, 'media': 36.00, 'grande': 47.00, 'familia': 53.00},
            'atualizar': True  # Existe, precisa atualizar preços
        },
        {
            'nome': 'Pizza Bacon com Milho',
            'ingredientes': 'Molho, mussarela, bacon, milho verde e orégano',
            'descricao': 'Combinação perfeita de bacon crocante com milho doce',
            'precos': {'pequena': 31.00, 'media': 38.00, 'grande': 49.00, 'familia': 55.00},
            'atualizar': False  # Nova pizza
        },
        {
            'nome': 'Pizza Baiana',
            'ingredientes': 'Molho, mussarela, calabresa ralada, pimenta calabresa, tomate em rodela e orégano',
            'descricao': 'Sabor picante típico da Bahia com pimenta calabresa',
            'precos': {'pequena': 29.00, 'media': 38.00, 'grande': 46.00, 'familia': 55.00},
            'atualizar': True  # Existe, precisa atualizar ingredientes e preços
        },
        {
            'nome': 'Pizza Bauru',
            'ingredientes': 'Molho, mussarela, presunto, milho verde, e orégano',
            'descricao': 'Inspirada no famoso sanduíche paulista',
            'precos': {'pequena': 28.00, 'media': 37.00, 'grande': 45.00, 'familia': 50.00},
            'atualizar': False  # Nova pizza
        },
        {
            'nome': 'Pizza Brasileira',
            'ingredientes': 'Molho, mussarela, ervilha, milho verde, palmito e orégano',
            'descricao': 'Sabores genuinamente brasileiros em uma pizza',
            'precos': {'pequena': 29.00, 'media': 38.00, 'grande': 43.00, 'familia': 49.00},
            'atualizar': False  # Nova pizza
        },
        {
            'nome': 'Pizza Brócolis',
            'ingredientes': 'Molho, mussarela, brócolis, e orégano',
            'descricao': 'Opção saudável com brócolis fresco',
            'precos': {'pequena': 32.00, 'media': 36.00, 'grande': 45.00, 'familia': 48.00},
            'atualizar': False  # Nova pizza
        },
        {
            'nome': 'Pizza Brócolis com Bacon',
            'ingredientes': 'Molho, mussarela, brócolis, bacon e orégano',
            'descricao': 'Combinação equilibrada de vegetais e bacon',
            'precos': {'pequena': 33.00, 'media': 38.00, 'grande': 46.00, 'familia': 49.00},
            'atualizar': False  # Nova pizza
        },
        {
            'nome': 'Pizza Calabresa',
            'ingredientes': 'Molho, mussarela, calabresa em rodelas, cebola e orégano',
            'descricao': 'A mais tradicional pizza brasileira',
            'precos': {'pequena': 28.00, 'media': 38.00, 'grande': 48.00, 'familia': 56.00},
            'atualizar': True  # Existe, precisa atualizar ingredientes e preços
        },
        {
            'nome': 'Pizza Calabresa ao Catupiry',
            'ingredientes': 'Molho, mussarela, calabresa, catupiry, cebola e orégano',
            'descricao': 'Calabresa tradicional com cremoso catupiry',
            'precos': {'pequena': 30.00, 'media': 39.00, 'grande': 49.00, 'familia': 57.00},
            'atualizar': False  # Nova pizza
        },
        {
            'nome': 'Pizza Calabresa com Cheddar',
            'ingredientes': 'Molho, mussarela, calabresa, cheddar, cebola e orégano',
            'descricao': 'Calabresa com o sabor intenso do cheddar',
            'precos': {'pequena': 32.00, 'media': 41.00, 'grande': 50.00, 'familia': 59.00},
            'atualizar': False  # Nova pizza
        },
        {
            'nome': 'Pizza Calabresa Paulista',
            'ingredientes': 'Molho, calabresa em rodelas, cebola e orégano',
            'descricao': 'Estilo paulista sem mussarela, mais tradicional',
            'precos': {'pequena': 27.00, 'media': 33.00, 'grande': 42.00, 'familia': 45.00},
            'atualizar': False  # Nova pizza
        },
        {
            'nome': 'Pizza Camarão',
            'ingredientes': 'Molho, mussarela, camarão refogado, vinagrete e orégano',
            'descricao': 'Camarões frescos refogados com vinagrete especial',
            'precos': {'pequena': 35.00, 'media': 39.00, 'grande': 50.00, 'familia': 59.00},
            'atualizar': True  # Existe, precisa atualizar ingredientes e preços
        },
        {
            'nome': 'Pizza Camarão ao Catupiry',
            'ingredientes': 'Molho, mussarela, camarão refogado, catupiry, vinagrete e orégano',
            'descricao': 'Camarão premium com catupiry cremoso',
            'precos': {'pequena': 38.00, 'media': 42.00, 'grande': 53.00, 'familia': 62.00},
            'atualizar': False  # Nova pizza
        },
        {
            'nome': 'Pizza Canadense',
            'ingredientes': 'Molho, mussarela, lombo canadense, abacaxi, catupiry, bacon e orégano',
            'descricao': 'Combinação exótica com lombo canadense e abacaxi',
            'precos': {'pequena': 34.00, 'media': 39.00, 'grande': 45.00, 'familia': 52.00},
            'atualizar': False  # Nova pizza
        }
    ]
    
    def atualizar_pizza_existente(pizza_data):
        """Atualizar pizza existente"""
        try:
            pizza = Produto.objects.get(nome=pizza_data['nome'])
            
            # Atualizar campos
            pizza.ingredientes = pizza_data['ingredientes']
            pizza.descricao = pizza_data['descricao']
            pizza.save()
            
            print(f"🔄 Pizza '{pizza.nome}' atualizada!")
            
            # Remover preços antigos e criar novos
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
            print(f"❌ Pizza '{pizza_data['nome']}' não encontrada para atualizar")
            return False
    
    def criar_pizza_nova(pizza_data):
        """Criar nova pizza"""
        try:
            # Verificar se já existe
            if Produto.objects.filter(nome=pizza_data['nome']).exists():
                print(f"❌ Pizza '{pizza_data['nome']}' já existe - pulando criação")
                return False
            
            # Criar produto
            pizza = Produto.objects.create(
                nome=pizza_data['nome'],
                categoria=categoria_salgadas,
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
    
    print("🍕 ATUALIZANDO CARDÁPIO DE PIZZAS 🍕")
    print("=" * 50)
    
    pizzas_atualizadas = 0
    pizzas_criadas = 0
    pizzas_erros = 0
    
    for pizza_data in pizzas_usuario:
        print(f"\n📝 Processando: {pizza_data['nome']}")
        
        if pizza_data['atualizar']:
            # Atualizar pizza existente
            if atualizar_pizza_existente(pizza_data):
                pizzas_atualizadas += 1
            else:
                pizzas_erros += 1
        else:
            # Criar nova pizza
            if criar_pizza_nova(pizza_data):
                pizzas_criadas += 1
            else:
                pizzas_erros += 1
    
    # Estatísticas finais
    print("\n" + "=" * 50)
    print("📊 RELATÓRIO FINAL")
    print("=" * 50)
    
    total_pizzas = Produto.objects.filter(tipo_produto='pizza').exclude(nome__icontains='PROMOCIONAL').count()
    total_promocionais = Produto.objects.filter(nome__icontains='PROMOCIONAL').count()
    
    print(f"🔄 Pizzas atualizadas: {pizzas_atualizadas}")
    print(f"✅ Pizzas criadas: {pizzas_criadas}")
    print(f"❌ Erros: {pizzas_erros}")
    print(f"🍕 Total de pizzas regulares: {total_pizzas}")
    print(f"🔥 Total de pizzas promocionais: {total_promocionais}")
    print(f"📊 Total geral: {total_pizzas + total_promocionais}")
    
    print("\n🎉 ATUALIZAÇÃO DO CARDÁPIO CONCLUÍDA! 🎉")

if __name__ == '__main__':
    atualizar_cardapio_pizzas()