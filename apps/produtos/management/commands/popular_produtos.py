from django.core.management.base import BaseCommand
from django.db import transaction
from apps.produtos.models import Produto, Categoria, Tamanho, ProdutoPreco
from decimal import Decimal


class Command(BaseCommand):
    help = 'Popula o banco de dados com produtos de exemplo'

    def handle(self, *args, **options):
        self.stdout.write('Iniciando população de produtos...')
        
        with transaction.atomic():
            # Criar categorias
            categorias = self.criar_categorias()
            
            # Criar tamanhos
            tamanhos = self.criar_tamanhos()
            
            # Criar produtos
            self.criar_pizzas(categorias, tamanhos)
            self.criar_bebidas(categorias)
            self.criar_bordas(categorias)
            self.criar_sobremesas(categorias)
            
        self.stdout.write(self.style.SUCCESS('Produtos populados com sucesso!'))
    
    def criar_categorias(self):
        self.stdout.write('Criando categorias...')
        
        categorias_data = [
            ('Pizzas Tradicionais', 'Receitas clássicas da casa'),
            ('Pizzas Especiais', 'Criações exclusivas do chef'),
            ('Bebidas', 'Refrigerantes, sucos e água'),
            ('Bordas Recheadas', 'Bordas especiais para sua pizza'),
            ('Sobremesas', 'Deliciosas sobremesas para finalizar'),
            ('Acompanhamentos', 'Petiscos e complementos'),
        ]
        
        categorias = {}
        for nome, descricao in categorias_data:
            categoria, created = Categoria.objects.get_or_create(
                nome=nome,
                defaults={'descricao': descricao, 'ativo': True}
            )
            categorias[nome] = categoria
            if created:
                self.stdout.write(f'  - Categoria "{nome}" criada')
        
        return categorias
    
    def criar_tamanhos(self):
        self.stdout.write('Criando tamanhos...')
        
        tamanhos_data = [
            ('Broto', 1),
            ('Média', 2),
            ('Grande', 3),
            ('Família', 4),
        ]
        
        tamanhos = {}
        for nome, ordem in tamanhos_data:
            tamanho, created = Tamanho.objects.get_or_create(
                nome=nome,
                defaults={'ordem': ordem, 'ativo': True}
            )
            tamanhos[nome] = tamanho
            if created:
                self.stdout.write(f'  - Tamanho "{nome}" criado')
        
        return tamanhos
    
    def criar_pizzas(self, categorias, tamanhos):
        self.stdout.write('Criando pizzas...')
        
        pizzas_tradicionais = [
            {
                'nome': 'Margherita',
                'descricao': 'Molho de tomate, mussarela, manjericão e azeite',
                'ingredientes': 'Molho de tomate, mussarela, manjericão fresco, azeite de oliva',
                'precos': {'Broto': 25.00, 'Média': 35.00, 'Grande': 45.00, 'Família': 55.00}
            },
            {
                'nome': 'Calabresa',
                'descricao': 'Molho de tomate, mussarela, calabresa e cebola',
                'ingredientes': 'Molho de tomate, mussarela, calabresa fatiada, cebola, orégano',
                'precos': {'Broto': 28.00, 'Média': 38.00, 'Grande': 48.00, 'Família': 58.00}
            },
            {
                'nome': 'Portuguesa',
                'descricao': 'Molho de tomate, mussarela, presunto, ovos, cebola, azeitona e orégano',
                'ingredientes': 'Molho de tomate, mussarela, presunto, ovos cozidos, cebola, azeitona preta, orégano',
                'precos': {'Broto': 30.00, 'Média': 40.00, 'Grande': 50.00, 'Família': 60.00}
            },
            {
                'nome': 'Quatro Queijos',
                'descricao': 'Molho de tomate, mussarela, provolone, parmesão e gorgonzola',
                'ingredientes': 'Molho de tomate, mussarela, provolone, parmesão, gorgonzola',
                'precos': {'Broto': 32.00, 'Média': 42.00, 'Grande': 52.00, 'Família': 62.00}
            },
        ]
        
        pizzas_especiais = [
            {
                'nome': 'Pizza do Chef',
                'descricao': 'Molho especial, mussarela de búfala, tomate seco, rúcula e lascas de parmesão',
                'ingredientes': 'Molho especial da casa, mussarela de búfala, tomate seco, rúcula fresca, lascas de parmesão',
                'precos': {'Broto': 35.00, 'Média': 45.00, 'Grande': 55.00, 'Família': 65.00}
            },
            {
                'nome': 'Camarão Premium',
                'descricao': 'Molho branco, mussarela, camarões grandes, alho e manjericão',
                'ingredientes': 'Molho branco, mussarela, camarões grandes, alho, manjericão, azeite trufado',
                'precos': {'Broto': 45.00, 'Média': 55.00, 'Grande': 65.00, 'Família': 75.00}
            },
        ]
        
        # Criar pizzas tradicionais
        for pizza_data in pizzas_tradicionais:
            pizza, created = Produto.objects.get_or_create(
                nome=pizza_data['nome'],
                categoria=categorias['Pizzas Tradicionais'],
                defaults={
                    'descricao': pizza_data['descricao'],
                    'tipo_produto': 'pizza',
                    'ingredientes': pizza_data['ingredientes'],
                    'ativo': True
                }
            )
            
            if created:
                # Criar preços por tamanho
                for tamanho_nome, preco in pizza_data['precos'].items():
                    ProdutoPreco.objects.create(
                        produto=pizza,
                        tamanho=tamanhos[tamanho_nome],
                        preco=Decimal(str(preco))
                    )
                self.stdout.write(f'  - Pizza "{pizza.nome}" criada')
        
        # Criar pizzas especiais
        for pizza_data in pizzas_especiais:
            pizza, created = Produto.objects.get_or_create(
                nome=pizza_data['nome'],
                categoria=categorias['Pizzas Especiais'],
                defaults={
                    'descricao': pizza_data['descricao'],
                    'tipo_produto': 'pizza',
                    'ingredientes': pizza_data['ingredientes'],
                    'ativo': True
                }
            )
            
            if created:
                # Criar preços por tamanho
                for tamanho_nome, preco in pizza_data['precos'].items():
                    ProdutoPreco.objects.create(
                        produto=pizza,
                        tamanho=tamanhos[tamanho_nome],
                        preco=Decimal(str(preco))
                    )
                self.stdout.write(f'  - Pizza especial "{pizza.nome}" criada')
    
    def criar_bebidas(self, categorias):
        self.stdout.write('Criando bebidas...')
        
        bebidas_data = [
            ('Coca-Cola Lata', 'Refrigerante Coca-Cola 350ml', 5.00),
            ('Coca-Cola 2L', 'Refrigerante Coca-Cola 2 litros', 12.00),
            ('Guaraná Antarctica Lata', 'Refrigerante Guaraná 350ml', 5.00),
            ('Suco de Laranja Natural', 'Suco de laranja natural 500ml', 8.00),
            ('Água Mineral', 'Água mineral sem gás 500ml', 3.00),
            ('Heineken Long Neck', 'Cerveja Heineken 330ml', 8.00),
        ]
        
        for nome, descricao, preco in bebidas_data:
            bebida, created = Produto.objects.get_or_create(
                nome=nome,
                categoria=categorias['Bebidas'],
                defaults={
                    'descricao': descricao,
                    'tipo_produto': 'bebida',
                    'preco_unitario': Decimal(str(preco)),
                    'estoque_disponivel': 50,
                    'ativo': True
                }
            )
            if created:
                self.stdout.write(f'  - Bebida "{nome}" criada')
    
    def criar_bordas(self, categorias):
        self.stdout.write('Criando bordas recheadas...')
        
        bordas_data = [
            ('Borda de Catupiry', 'Borda recheada com catupiry original cremoso', 8.00),
            ('Borda de Cheddar', 'Borda recheada com cheddar derretido', 8.00),
            ('Borda de Chocolate', 'Borda doce recheada com chocolate ao leite', 10.00),
            ('Borda de Cream Cheese', 'Borda recheada com cream cheese temperado', 9.00),
            ('Borda de Alho', 'Borda temperada com alho e ervas finas', 6.00),
            ('Borda de Doce de Leite', 'Borda doce recheada com doce de leite', 11.00),
        ]
        
        for nome, descricao, preco in bordas_data:
            borda, created = Produto.objects.get_or_create(
                nome=nome,
                categoria=categorias['Bordas Recheadas'],
                defaults={
                    'descricao': descricao,
                    'tipo_produto': 'borda',
                    'preco_unitario': Decimal(str(preco)),
                    'ativo': True
                }
            )
            if created:
                self.stdout.write(f'  - Borda "{nome}" criada')
    
    def criar_sobremesas(self, categorias):
        self.stdout.write('Criando sobremesas...')
        
        sobremesas_data = [
            ('Pizza de Chocolate', 'Pizza doce com chocolate ao leite e morangos', 35.00),
            ('Brownie com Sorvete', 'Brownie quentinho com sorvete de creme', 18.00),
            ('Petit Gateau', 'Bolinho de chocolate com sorvete', 22.00),
        ]
        
        for nome, descricao, preco in sobremesas_data:
            sobremesa, created = Produto.objects.get_or_create(
                nome=nome,
                categoria=categorias['Sobremesas'],
                defaults={
                    'descricao': descricao,
                    'tipo_produto': 'sobremesa',
                    'preco_unitario': Decimal(str(preco)),
                    'ativo': True
                }
            )
            if created:
                self.stdout.write(f'  - Sobremesa "{nome}" criada')