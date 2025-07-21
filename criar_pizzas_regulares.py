#!/usr/bin/env python
"""
Script para criar pizzas regulares (não promocionais) com preços por tamanho
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoProject.settings')
django.setup()

from apps.produtos.models import Produto, Categoria, ProdutoPreco, Tamanho
from decimal import Decimal

def criar_pizzas_regulares():
    """Criar pizzas regulares com preços por tamanho"""
    
    # Obter categorias
    categoria_salgadas = Categoria.objects.get(nome='Pizzas Salgadas')
    categoria_doces = Categoria.objects.get(nome='Pizzas Doces')
    categoria_especiais = Categoria.objects.get(nome='Pizzas Especiais')
    
    # Obter tamanhos
    tamanhos = {
        'pequena': Tamanho.objects.get(nome='Pequena'),
        'media': Tamanho.objects.get(nome='Média'),
        'grande': Tamanho.objects.get(nome='Grande'),
        'familia': Tamanho.objects.get(nome='Família'),
    }
    
    # Definir pizzas salgadas tradicionais
    pizzas_salgadas = [
        {
            'nome': 'Pizza Marguerita',
            'ingredientes': 'Molho de tomate, mussarela, tomate, manjericão, azeitona',
            'descricao': 'Clássica pizza italiana com sabores frescos',
            'precos': {'pequena': 25.00, 'media': 35.00, 'grande': 45.00, 'familia': 55.00}
        },
        {
            'nome': 'Pizza Calabresa',
            'ingredientes': 'Molho de tomate, mussarela, calabresa, cebola, azeitona',
            'descricao': 'Traditional brasileira com calabresa artesanal',
            'precos': {'pequena': 28.00, 'media': 38.00, 'grande': 48.00, 'familia': 58.00}
        },
        {
            'nome': 'Pizza Portuguesa',
            'ingredientes': 'Molho de tomate, mussarela, presunto, ovos, cebola, azeitona, ervilha',
            'descricao': 'Sabor tradicional português com ingredientes selecionados',
            'precos': {'pequena': 32.00, 'media': 42.00, 'grande': 52.00, 'familia': 62.00}
        },
        {
            'nome': 'Pizza Frango ao Catupiry',
            'ingredientes': 'Molho de tomate, mussarela, frango desfiado, catupiry, azeitona',
            'descricao': 'Frango temperado com o cremoso catupiry original',
            'precos': {'pequena': 30.00, 'media': 40.00, 'grande': 50.00, 'familia': 60.00}
        },
        {
            'nome': 'Pizza Bacon',
            'ingredientes': 'Molho de tomate, mussarela, bacon crocante, cebola, azeitona',
            'descricao': 'Bacon defumado crocante para os amantes de sabor intenso',
            'precos': {'pequena': 29.00, 'media': 39.00, 'grande': 49.00, 'familia': 59.00}
        },
        {
            'nome': 'Pizza Atum',
            'ingredientes': 'Molho de tomate, mussarela, atum, cebola, azeitona',
            'descricao': 'Atum selecionado com temperos especiais',
            'precos': {'pequena': 31.00, 'media': 41.00, 'grande': 51.00, 'familia': 61.00}
        },
        {
            'nome': 'Pizza Mussarela',
            'ingredientes': 'Molho de tomate, mussarela especial, tomate, azeitona',
            'descricao': 'Simplicidade e sabor com mussarela de primeira qualidade',
            'precos': {'pequena': 24.00, 'media': 34.00, 'grande': 44.00, 'familia': 54.00}
        },
        {
            'nome': 'Pizza Baiana',
            'ingredientes': 'Molho de tomate, mussarela, calabresa, pimenta, cebola, azeitona',
            'descricao': 'Sabor picante típico da Bahia',
            'precos': {'pequena': 30.00, 'media': 40.00, 'grande': 50.00, 'familia': 60.00}
        },
        {
            'nome': 'Pizza Napolitana',
            'ingredientes': 'Molho de tomate, mussarela, tomate, parmesão, manjericão, azeitona',
            'descricao': 'Estilo napolitano com queijo parmesão',
            'precos': {'pequena': 27.00, 'media': 37.00, 'grande': 47.00, 'familia': 57.00}
        },
        {
            'nome': 'Pizza Milho Verde',
            'ingredientes': 'Molho de tomate, mussarela, milho verde, azeitona',
            'descricao': 'Doçura natural do milho verde selecionado',
            'precos': {'pequena': 26.00, 'media': 36.00, 'grande': 46.00, 'familia': 56.00}
        }
    ]
    
    # Definir pizzas doces
    pizzas_doces = [
        {
            'nome': 'Pizza Chocolate',
            'ingredientes': 'Chocolate ao leite derretido, granulado',
            'descricao': 'Irresistível cobertura de chocolate cremoso',
            'precos': {'pequena': 22.00, 'media': 32.00, 'grande': 42.00, 'familia': 52.00}
        },
        {
            'nome': 'Pizza Banana Caramelizada',
            'ingredientes': 'Banana caramelizada, canela, açúcar cristal',
            'descricao': 'Bananas frescas caramelizadas na hora',
            'precos': {'pequena': 24.00, 'media': 34.00, 'grande': 44.00, 'familia': 54.00}
        },
        {
            'nome': 'Pizza Romeu e Julieta',
            'ingredientes': 'Queijo minas, goiabada cremosa',
            'descricao': 'Clássica combinação mineira doce e salgada',
            'precos': {'pequena': 26.00, 'media': 36.00, 'grande': 46.00, 'familia': 56.00}
        },
        {
            'nome': 'Pizza Brigadeiro',
            'ingredientes': 'Brigadeiro cremoso, granulado, morango',
            'descricao': 'O doce mais amado do Brasil em versão pizza',
            'precos': {'pequena': 28.00, 'media': 38.00, 'grande': 48.00, 'familia': 58.00}
        }
    ]
    
    # Definir pizzas especiais
    pizzas_especiais = [
        {
            'nome': 'Pizza Quatro Queijos',
            'ingredientes': 'Mussarela, parmesão, gorgonzola, catupiry, azeitona',
            'descricao': 'Combinação irresistível de quatro queijos nobres',
            'precos': {'pequena': 35.00, 'media': 45.00, 'grande': 55.00, 'familia': 65.00}
        },
        {
            'nome': 'Pizza Camarão',
            'ingredientes': 'Molho de tomate, mussarela, camarão refogado, catupiry, azeitona',
            'descricao': 'Camarões frescos refogados com temperos especiais',
            'precos': {'pequena': 42.00, 'media': 52.00, 'grande': 62.00, 'familia': 72.00}
        },
        {
            'nome': 'Pizza Salmão',
            'ingredientes': 'Molho branco, mussarela, salmão defumado, alcaparras, cream cheese',
            'descricao': 'Salmão defumado premium com cream cheese',
            'precos': {'pequena': 45.00, 'media': 55.00, 'grande': 65.00, 'familia': 75.00}
        },
        {
            'nome': 'Pizza Vegetariana',
            'ingredientes': 'Molho de tomate, mussarela, abobrinha, berinjela, pimentão, tomate seco, azeitona',
            'descricao': 'Seleção de vegetais frescos grelhados',
            'precos': {'pequena': 33.00, 'media': 43.00, 'grande': 53.00, 'familia': 63.00}
        },
        {
            'nome': 'Pizza Carbonara',
            'ingredientes': 'Molho branco, mussarela, bacon, ovos, parmesão, azeitona',
            'descricao': 'Clássico italiano com molho carbonara autêntico',
            'precos': {'pequena': 36.00, 'media': 46.00, 'grande': 56.00, 'familia': 66.00}
        }
    ]
    
    def criar_pizzas_categoria(pizzas_data, categoria):
        """Criar pizzas de uma categoria específica"""
        print(f"\n=== Criando pizzas da categoria: {categoria.nome} ===")
        
        for pizza_data in pizzas_data:
            # Verificar se já existe
            if Produto.objects.filter(nome=pizza_data['nome']).exists():
                print(f"❌ Pizza '{pizza_data['nome']}' já existe - pulando")
                continue
            
            # Criar produto
            pizza = Produto.objects.create(
                nome=pizza_data['nome'],
                categoria=categoria,
                tipo_produto='pizza',
                descricao=pizza_data['descricao'],
                ingredientes=pizza_data['ingredientes'],
                ativo=True
            )
            
            print(f"✅ Pizza '{pizza.nome}' criada com sucesso!")
            
            # Criar preços por tamanho
            for tamanho_nome, preco in pizza_data['precos'].items():
                if tamanho_nome in tamanhos:
                    ProdutoPreco.objects.create(
                        produto=pizza,
                        tamanho=tamanhos[tamanho_nome],
                        preco=Decimal(str(preco))
                    )
                    print(f"   - {tamanhos[tamanho_nome].nome}: R$ {preco:.2f}")
    
    print("🍕 INICIANDO CRIAÇÃO DE PIZZAS REGULARES 🍕")
    print("=" * 50)
    
    # Criar todas as categorias
    criar_pizzas_categoria(pizzas_salgadas, categoria_salgadas)
    criar_pizzas_categoria(pizzas_doces, categoria_doces)  
    criar_pizzas_categoria(pizzas_especiais, categoria_especiais)
    
    # Estatísticas finais
    print("\n" + "=" * 50)
    print("📊 RELATÓRIO FINAL")
    print("=" * 50)
    
    total_pizzas = Produto.objects.filter(tipo_produto='pizza').exclude(nome__icontains='PROMOCIONAL').count()
    total_promocionais = Produto.objects.filter(nome__icontains='PROMOCIONAL').count()
    
    print(f"✅ Pizzas regulares criadas: {total_pizzas}")
    print(f"🔥 Pizzas promocionais existentes: {total_promocionais}")
    print(f"🍕 Total de pizzas no sistema: {total_pizzas + total_promocionais}")
    
    # Contagem por categoria
    for categoria in [categoria_salgadas, categoria_doces, categoria_especiais]:
        count = Produto.objects.filter(categoria=categoria, tipo_produto='pizza').exclude(nome__icontains='PROMOCIONAL').count()
        print(f"   - {categoria.nome}: {count} pizzas")
    
    print("\n🎉 PROCESSO CONCLUÍDO COM SUCESSO! 🎉")

if __name__ == '__main__':
    criar_pizzas_regulares()