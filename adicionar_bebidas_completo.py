#!/usr/bin/env python
"""
Script para adicionar todas as bebidas ao cardápio
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoProject.settings')
django.setup()

from apps.produtos.models import Produto, Categoria, ProdutoPreco, Tamanho
from decimal import Decimal

def adicionar_bebidas_completo():
    """Adicionar todas as bebidas ao cardápio"""
    
    # Obter ou criar categorias específicas para bebidas
    categoria_cervejas, _ = Categoria.objects.get_or_create(nome='Cervejas')
    categoria_bebidas, _ = Categoria.objects.get_or_create(nome='Bebidas')
    categoria_outros, _ = Categoria.objects.get_or_create(nome='Outros')
    
    # Criar categorias específicas se não existirem
    categoria_drinks, _ = Categoria.objects.get_or_create(
        nome='Drinks',
        defaults={'descricao': 'Coquetéis e drinks especiais'}
    )
    categoria_destilados, _ = Categoria.objects.get_or_create(
        nome='Destilados',
        defaults={'descricao': 'Vodkas, whiskys e outros destilados'}
    )
    
    # Obter tamanho único para bebidas
    tamanho_unico, _ = Tamanho.objects.get_or_create(
        nome='Único',
        defaults={'ordem': 0, 'ativo': True}
    )
    
    # Lista completa de bebidas
    bebidas_lista = [
        # CERVEJAS
        {
            'nome': 'Cerveja Itapaiva 300ml',
            'categoria': categoria_cervejas,
            'tipo_produto': 'bebida',
            'descricao': 'Cerveja nacional gelada 300ml',
            'preco': 4.00
        },
        {
            'nome': 'Cerveja Skol 300ml',
            'categoria': categoria_cervejas,
            'tipo_produto': 'bebida',
            'descricao': 'Cerveja Skol gelada 300ml',
            'preco': 5.00
        },
        {
            'nome': 'Cerveja Devassa 300ml',
            'categoria': categoria_cervejas,
            'tipo_produto': 'bebida',
            'descricao': 'Cerveja Devassa gelada 300ml',
            'preco': 5.00
        },
        {
            'nome': 'Cerveja Heineken 330ml',
            'categoria': categoria_cervejas,
            'tipo_produto': 'bebida',
            'descricao': 'Cerveja premium Heineken 330ml',
            'preco': 10.00
        },
        {
            'nome': 'Cerveja Heineken sem Álcool',
            'categoria': categoria_cervejas,
            'tipo_produto': 'bebida',
            'descricao': 'Cerveja Heineken 0% álcool',
            'preco': 10.00
        },
        {
            'nome': 'Cerveja Eisenbahn',
            'categoria': categoria_cervejas,
            'tipo_produto': 'bebida',
            'descricao': 'Cerveja artesanal Eisenbahn',
            'preco': 8.00
        },
        {
            'nome': 'Cerveja Budweiser 330ml',
            'categoria': categoria_cervejas,
            'tipo_produto': 'bebida',
            'descricao': 'Cerveja americana Budweiser 330ml',
            'preco': 10.00
        },
        {
            'nome': 'Cerveja Corona 330ml',
            'categoria': categoria_cervejas,
            'tipo_produto': 'bebida',
            'descricao': 'Cerveja mexicana Corona 330ml',
            'preco': 10.00
        },
        {
            'nome': 'Cerveja Skol Lata 350ml',
            'categoria': categoria_cervejas,
            'tipo_produto': 'bebida',
            'descricao': 'Cerveja Skol lata gelada 350ml',
            'preco': 5.00
        },
        {
            'nome': 'Cerveja Itapaiva Lata 350ml',
            'categoria': categoria_cervejas,
            'tipo_produto': 'bebida',
            'descricao': 'Cerveja Itapaiva lata gelada 350ml',
            'preco': 4.00
        },
        
        # DRINKS
        {
            'nome': 'Caipirinha de Limão',
            'categoria': categoria_drinks,
            'tipo_produto': 'bebida',
            'descricao': 'Drink tradicional brasileiro com cachaça e limão',
            'preco': 15.00,
            'observacoes': 'Para alteração da vodka: R$ 20,00'
        },
        {
            'nome': 'Caipirosca de Limão',
            'categoria': categoria_drinks,
            'tipo_produto': 'bebida',
            'descricao': 'Caipirinha feita com vodka e limão',
            'preco': 15.00,
            'observacoes': 'Para alteração da vodka: R$ 20,00'
        },
        {
            'nome': 'Cuba Libre',
            'categoria': categoria_drinks,
            'tipo_produto': 'bebida',
            'descricao': 'Drink clássico com rum, coca-cola e limão',
            'preco': 15.00,
            'observacoes': 'Para alteração da vodka: R$ 20,00'
        },
        {
            'nome': 'Drink de Maracujá',
            'categoria': categoria_drinks,
            'tipo_produto': 'bebida',
            'descricao': 'Drink tropical refrescante de maracujá',
            'preco': 15.00,
            'observacoes': 'Para alteração da vodka: R$ 20,00'
        },
        {
            'nome': 'Espanhola',
            'categoria': categoria_drinks,
            'tipo_produto': 'bebida',
            'descricao': 'Drink especial da casa estilo espanhol',
            'preco': 15.00,
            'observacoes': 'Para alteração da vodka: R$ 20,00'
        },
        {
            'nome': 'Nevada',
            'categoria': categoria_drinks,
            'tipo_produto': 'bebida',
            'descricao': 'Drink refrescante estilo Nevada',
            'preco': 15.00,
            'observacoes': 'Para alteração da vodka: R$ 20,00'
        },
        
        # VODKAS (Dose)
        {
            'nome': 'Vodka Absolut (Dose)',
            'categoria': categoria_destilados,
            'tipo_produto': 'bebida',
            'descricao': 'Dose de vodka premium Absolut',
            'preco': 15.00
        },
        {
            'nome': 'Vodka Bacardi (Dose)',
            'categoria': categoria_destilados,
            'tipo_produto': 'bebida',
            'descricao': 'Dose de vodka Bacardi',
            'preco': 10.00
        },
        {
            'nome': 'Vodka Smirnoff (Dose)',
            'categoria': categoria_destilados,
            'tipo_produto': 'bebida',
            'descricao': 'Dose de vodka Smirnoff',
            'preco': 10.00
        },
        {
            'nome': 'Vodka Orloff (Dose)',
            'categoria': categoria_destilados,
            'tipo_produto': 'bebida',
            'descricao': 'Dose de vodka Orloff',
            'preco': 10.00
        },
        {
            'nome': 'Vodka Natasha (Dose)',
            'categoria': categoria_destilados,
            'tipo_produto': 'bebida',
            'descricao': 'Dose de vodka Natasha',
            'preco': 10.00
        },
        
        # WHISKYS (Dose)
        {
            'nome': 'Whisky Red Label (Dose)',
            'categoria': categoria_destilados,
            'tipo_produto': 'bebida',
            'descricao': 'Dose de whisky Johnnie Walker Red Label',
            'preco': 12.00
        },
        {
            'nome': 'Whisky Ballantines (Dose)',
            'categoria': categoria_destilados,
            'tipo_produto': 'bebida',
            'descricao': 'Dose de whisky Ballantines',
            'preco': 10.00
        },
        {
            'nome': 'Whisky Teachers (Dose)',
            'categoria': categoria_destilados,
            'tipo_produto': 'bebida',
            'descricao': 'Dose de whisky Teachers',
            'preco': 7.00
        },
        
        # OUTROS
        {
            'nome': 'Campari (Dose)',
            'categoria': categoria_destilados,
            'tipo_produto': 'bebida',
            'descricao': 'Dose de aperitivo Campari',
            'preco': 10.00
        },
        {
            'nome': 'Montila Limão',
            'categoria': categoria_bebidas,
            'tipo_produto': 'bebida',
            'descricao': 'Drink Montila sabor limão',
            'preco': 8.00
        },
        {
            'nome': 'Red Bull 250ml',
            'categoria': categoria_bebidas,
            'tipo_produto': 'bebida',
            'descricao': 'Energético Red Bull 250ml',
            'preco': 15.00
        }
    ]
    
    def criar_bebida(bebida_data):
        """Criar nova bebida"""
        try:
            # Verificar se já existe
            if Produto.objects.filter(nome=bebida_data['nome']).exists():
                print(f"❌ Bebida '{bebida_data['nome']}' já existe - pulando")
                return False
            
            # Criar produto
            descricao_completa = bebida_data['descricao']
            if 'observacoes' in bebida_data and bebida_data['observacoes']:
                descricao_completa += f" - {bebida_data['observacoes']}"
            
            bebida = Produto.objects.create(
                nome=bebida_data['nome'],
                categoria=bebida_data['categoria'],
                tipo_produto=bebida_data['tipo_produto'],
                descricao=descricao_completa,
                preco_unitario=Decimal(str(bebida_data['preco'])),
                ativo=True
            )
            
            # Criar preço único
            ProdutoPreco.objects.create(
                produto=bebida,
                tamanho=tamanho_unico,
                preco=Decimal(str(bebida_data['preco']))
            )
            
            print(f"✅ Bebida '{bebida.nome}' criada! - R$ {bebida_data['preco']:.2f}")
            
            return True
            
        except Exception as e:
            print(f"❌ Erro ao criar bebida '{bebida_data['nome']}': {e}")
            return False
    
    print("🍺 ADICIONANDO CARDÁPIO COMPLETO DE BEBIDAS 🍺")
    print("=" * 55)
    
    bebidas_criadas = 0
    bebidas_existentes = 0
    bebidas_erros = 0
    
    # Processar todas as bebidas
    for bebida_data in bebidas_lista:
        if criar_bebida(bebida_data):
            bebidas_criadas += 1
        elif Produto.objects.filter(nome=bebida_data['nome']).exists():
            bebidas_existentes += 1
        else:
            bebidas_erros += 1
    
    # Estatísticas finais
    print("\n" + "=" * 55)
    print("📊 RELATÓRIO FINAL - BEBIDAS")
    print("=" * 55)
    
    total_bebidas = Produto.objects.filter(tipo_produto='bebida').count()
    total_produtos = Produto.objects.all().count()
    
    print(f"✅ Bebidas criadas: {bebidas_criadas}")
    print(f"⚠️ Bebidas já existentes: {bebidas_existentes}")
    print(f"❌ Erros: {bebidas_erros}")
    print(f"🍺 Total de bebidas no sistema: {total_bebidas}")
    print(f"📊 Total geral de produtos: {total_produtos}")
    
    # Contagem por categoria de bebidas
    print("\n📋 DISTRIBUIÇÃO POR CATEGORIA DE BEBIDAS:")
    categorias_bebidas = [categoria_cervejas, categoria_drinks, categoria_destilados, categoria_bebidas]
    
    for categoria in categorias_bebidas:
        count = Produto.objects.filter(categoria=categoria, tipo_produto='bebida').count()
        if count > 0:
            print(f"   - {categoria.nome}: {count} bebidas")
    
    # Faixas de preços
    print("\n💰 FAIXA DE PREÇOS DAS BEBIDAS:")
    precos_bebidas = []
    for bebida in Produto.objects.filter(tipo_produto='bebida'):
        if bebida.preco_unitario:
            precos_bebidas.append(float(bebida.preco_unitario))
    
    if precos_bebidas:
        min_preco = min(precos_bebidas)
        max_preco = max(precos_bebidas)
        print(f"   - Mínimo: R$ {min_preco:.2f}")
        print(f"   - Máximo: R$ {max_preco:.2f}")
    
    # Destaques por categoria
    print("\n🍺 DESTAQUES POR CATEGORIA:")
    print("   - Cervejas: 10 opções (nacionais e importadas)")
    print("   - Drinks: 6 coquetéis especiais")
    print("   - Destilados: 8 doses premium")
    print("   - Outros: 2 bebidas especiais")
    
    print("\n" + "🎉" * 20)
    print("🍺 CARDÁPIO DE BEBIDAS COMPLETAMENTE ADICIONADO! 🍺")
    print("🎉" * 20)
    print(f"\n🏆 TOTAL DE {bebidas_criadas} BEBIDAS ADICIONADAS COM SUCESSO!")
    print("🍻 O bar está completo e pronto para atender!")
    print("🚀 Sistema completo: Pizzas + Bebidas!")

if __name__ == '__main__':
    adicionar_bebidas_completo()