#!/usr/bin/env python
"""
Script para adicionar a quarta e última parte das pizzas fornecidas pelo usuário
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoProject.settings')
django.setup()

from apps.produtos.models import Produto, Categoria, ProdutoPreco, Tamanho
from decimal import Decimal

def adicionar_pizzas_parte4_final():
    """Adicionar quarta e última lista de pizzas"""
    
    # Obter categorias
    categoria_salgadas = Categoria.objects.get(nome='Pizzas Salgadas')
    categoria_especiais = Categoria.objects.get(nome='Pizzas Especiais')
    categoria_tradicionais = Categoria.objects.get(nome='Pizzas Tradicionais')
    
    # Obter tamanhos
    tamanhos = {
        'pequena': Tamanho.objects.get(nome='Pequena'),
        'media': Tamanho.objects.get(nome='Média'),
        'grande': Tamanho.objects.get(nome='Grande'),
        'familia': Tamanho.objects.get(nome='Família'),
    }
    
    # Quarta e última lista de pizzas do usuário
    pizzas_parte4 = [
        {
            'nome': 'Pizza Palmito',
            'categoria': categoria_salgadas,
            'ingredientes': 'Molho, mussarela, palmito e orégano',
            'descricao': 'Sabor clássico com palmito de primeira qualidade',
            'precos': {'pequena': 30.00, 'media': 35.00, 'grande': 43.00, 'familia': 48.00}
        },
        {
            'nome': 'Pizza Palmito com Milho Verde',
            'categoria': categoria_salgadas,
            'ingredientes': 'Molho, mussarela, palmito, milho verde, tomate e orégano',
            'descricao': 'Combinação refrescante de palmito com milho doce',
            'precos': {'pequena': 32.00, 'media': 37.00, 'grande': 45.00, 'familia': 50.00}
        },
        {
            'nome': 'Pizza Portuguesa com Palmito',
            'categoria': categoria_especiais,
            'ingredientes': 'Molho, mussarela, presunto, cebola, vinagrete, milho verde, ovos, palmito, pimentão e orégano',
            'descricao': 'Portuguesa tradicional enriquecida com palmito',
            'precos': {'pequena': 35.00, 'media': 39.00, 'grande': 47.00, 'familia': 55.00}
        },
        {
            'nome': 'Pizza PortuguAtum',
            'categoria': categoria_especiais,
            'ingredientes': 'Molho, mussarela, vinagrete, milho verde, ovos, atum, cebola e orégano',
            'descricao': 'Fusão inovadora da portuguesa com atum selecionado',
            'precos': {'pequena': 37.00, 'media': 41.00, 'grande': 48.00, 'familia': 56.00}
        },
        {
            'nome': 'Pizza Provolone com Bacon',
            'categoria': categoria_especiais,
            'ingredientes': 'Molho, mussarela, provolone, bacon e orégano',
            'descricao': 'Sabor intenso do provolone com bacon crocante',
            'precos': {'pequena': 33.00, 'media': 38.00, 'grande': 43.00, 'familia': 47.00}
        },
        {
            'nome': 'Pizza Talentosa',
            'categoria': categoria_especiais,
            'ingredientes': 'Molho, mussarela, calabresa moída, frango, cerejas e orégano',
            'descricao': 'Criação única com toque doce das cerejas',
            'precos': {'pequena': 30.00, 'media': 37.00, 'grande': 48.00, 'familia': 57.00}
        },
        {
            'nome': 'Pizza Tomate Seco',
            'categoria': categoria_salgadas,
            'ingredientes': 'Molho, mussarela, tomate seco e orégano',
            'descricao': 'Sabor concentrado e especial do tomate seco',
            'precos': {'pequena': 28.00, 'media': 33.00, 'grande': 38.00, 'familia': 45.00}
        },
        {
            'nome': 'Pizza Tomate Seco à Parmesão',
            'categoria': categoria_especiais,
            'ingredientes': 'Molho, mussarela, tomate seco, parmesão e orégano',
            'descricao': 'Tomate seco com toque nobre do parmesão',
            'precos': {'pequena': 32.00, 'media': 38.00, 'grande': 43.00, 'familia': 52.00}
        },
        {
            'nome': 'Pizza Toscana',
            'categoria': categoria_salgadas,
            'ingredientes': 'Molho, mussarela, calabresa ralada, ovo ralado, cebola e orégano',
            'descricao': 'Receita toscana com ovos e calabresa ralada',
            'precos': {'pequena': 30.00, 'media': 36.00, 'grande': 45.00, 'familia': 53.00}
        },
        {
            'nome': 'Pizza Tropical',
            'categoria': categoria_salgadas,
            'ingredientes': 'Molho, mussarela, calabresa, palmito, azeitona sem caroço e orégano',
            'descricao': 'Sabores tropicais com calabresa e palmito',
            'precos': {'pequena': 32.00, 'media': 38.00, 'grande': 46.00, 'familia': 53.00}
        },
        {
            'nome': 'Pizza do Cliente',
            'categoria': categoria_especiais,
            'ingredientes': 'Molho, mussarela e até 5 ingredientes à escolha do cliente',
            'descricao': 'Seja o chefe, use sua criatividade e monte sua pizza com até 5 ingredientes',
            'precos': {'pequena': 38.00, 'media': 45.00, 'grande': 58.00, 'familia': 70.00}
        }
    ]
    
    # Pizzas que precisam ser atualizadas (já existem)
    pizzas_atualizar = [
        {
            'nome': 'Pizza Portuguesa',
            'ingredientes': 'Molho, mussarela, presunto, cebola, vinagrete, milho verde, ovos, pimentão e orégano',
            'descricao': 'Sabor tradicional português com ingredientes selecionados',
            'precos': {'pequena': 33.00, 'media': 37.00, 'grande': 45.00, 'familia': 52.00}
        },
        {
            'nome': 'Pizza Vegetariana',
            'ingredientes': 'Molho, mussarela, brócolis, palmito, milho, ervilha, tomate e orégano',
            'descricao': 'Seleção de vegetais frescos e nutritivos',
            'precos': {'pequena': 28.00, 'media': 34.00, 'grande': 40.00, 'familia': 49.00}
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
    
    print("🍕 ADICIONANDO QUARTA E ÚLTIMA PARTE DAS PIZZAS 🍕")
    print("=" * 55)
    
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
    for pizza_data in pizzas_parte4:
        print(f"\n📝 Processando: {pizza_data['nome']}")
        
        if criar_pizza(pizza_data):
            pizzas_criadas += 1
        else:
            pizzas_erros += 1
    
    # Estatísticas finais
    print("\n" + "=" * 55)
    print("📊 RELATÓRIO FINAL - PARTE 4 (ÚLTIMA)")
    print("=" * 55)
    
    total_pizzas = Produto.objects.filter(tipo_produto='pizza').exclude(nome__icontains='PROMOCIONAL').count()
    total_promocionais = Produto.objects.filter(nome__icontains='PROMOCIONAL').count()
    
    print(f"🔄 Pizzas atualizadas: {pizzas_atualizadas}")
    print(f"✅ Pizzas criadas: {pizzas_criadas}")
    print(f"❌ Erros: {pizzas_erros}")
    print(f"🍕 Total de pizzas regulares: {total_pizzas}")
    print(f"🔥 Total de pizzas promocionais: {total_promocionais}")
    print(f"📊 TOTAL GERAL NO SISTEMA: {total_pizzas + total_promocionais}")
    
    # Contagem detalhada por categoria
    print("\n📋 DISTRIBUIÇÃO FINAL POR CATEGORIA:")
    all_categories = Categoria.objects.all()
    for categoria in all_categories:
        count = Produto.objects.filter(categoria=categoria, tipo_produto='pizza').exclude(nome__icontains='PROMOCIONAL').count()
        if count > 0:
            print(f"   - {categoria.nome}: {count} pizzas")
    
    # Estatísticas de preços
    print("\n💰 FAIXA DE PREÇOS FINAL:")
    all_pizzas = Produto.objects.filter(tipo_produto='pizza').exclude(nome__icontains='PROMOCIONAL').prefetch_related('precos')
    
    precos_por_tamanho = {'pequena': [], 'media': [], 'grande': [], 'familia': []}
    
    for pizza in all_pizzas:
        for preco in pizza.precos.all():
            tamanho_nome = preco.tamanho.nome.lower()
            if tamanho_nome in precos_por_tamanho:
                precos_por_tamanho[tamanho_nome].append(float(preco.preco))
    
    for tamanho, precos_list in precos_por_tamanho.items():
        if precos_list:
            min_preco = min(precos_list)
            max_preco = max(precos_list)
            print(f"   - {tamanho.capitalize()}: R$ {min_preco:.2f} - R$ {max_preco:.2f}")
    
    print("\n" + "🎉" * 20)
    print("🍕 CARDÁPIO DE PIZZAS COMPLETAMENTE FINALIZADO! 🍕")
    print("🎉" * 20)
    print(f"\n🏆 TOTAL DE {total_pizzas + total_promocionais} PIZZAS CRIADAS COM SUCESSO!")
    print("📝 O sistema está pronto para atender todos os clientes!")
    print("🚀 Pronto para produção!")

if __name__ == '__main__':
    adicionar_pizzas_parte4_final()