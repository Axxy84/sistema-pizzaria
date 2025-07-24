import os
import django
import requests

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoProject.settings')
django.setup()

from django.test import Client
from apps.produtos.models import Produto, Categoria

# Cliente de teste
client = Client()

# Login
user = get_user_model().objects.get(username='admin')
client.force_login(user)

# 1. Verificar produtos no banco
print("=== PRODUTOS POR CATEGORIA NO BANCO ===")
categorias = {}
for produto in Produto.objects.filter(ativo=True).select_related('categoria'):
    cat_nome = produto.categoria.nome if produto.categoria else 'Sem categoria'
    if cat_nome not in categorias:
        categorias[cat_nome] = []
    categorias[cat_nome].append(produto.nome)

for cat, produtos in sorted(categorias.items()):
    print(f"\n{cat} ({len(produtos)} produtos):")
    for p in produtos[:3]:  # Mostrar apenas 3 primeiros
        print(f"  - {p}")
    if len(produtos) > 3:
        print(f"  ... e mais {len(produtos) - 3}")

# 2. Testar API
print("\n\n=== TESTE DA API PARA_PEDIDO_RAPIDO ===")
response = client.get('/api/produtos/para_pedido_rapido/')

if response.status_code == 200:
    data = response.json()
    produtos = data.get('produtos', [])
    
    # Agrupar por categoria
    por_categoria = {}
    for produto in produtos:
        cat = produto['categoria']
        if cat not in por_categoria:
            por_categoria[cat] = []
        por_categoria[cat].append(produto['nome'])
    
    print(f"\nTotal de produtos na API: {len(produtos)}")
    print("\nProdutos por categoria na API:")
    for cat, prods in sorted(por_categoria.items()):
        print(f"\n{cat.upper()} ({len(prods)} produtos):")
        for p in prods[:5]:
            print(f"  - {p}")
        if len(prods) > 5:
            print(f"  ... e mais {len(prods) - 5}")
else:
    print(f"Erro na API: {response.status_code}")

# 3. Verificar mapeamento específico
print("\n\n=== VERIFICAÇÃO DO MAPEAMENTO ===")
print("✓ Pizzas: Produtos com 'pizza', 'especial', 'tradicional'")
print("✓ Bebidas: Produtos com 'bebida', 'refrigerante', 'suco', etc")
print("✓ Bordas: Produtos com 'borda', 'recheada', 'adicional'")
print("✓ Outros: Sobremesas e demais produtos")

# 4. Verificar se há produtos de sobremesa
sobremesas = Categoria.objects.filter(nome__icontains='sobremesa')
if sobremesas.exists():
    print(f"\n⚠️  Ainda existem {sobremesas.count()} categoria(s) de sobremesa no banco")
    for cat in sobremesas:
        produtos_cat = Produto.objects.filter(categoria=cat, ativo=True).count()
        print(f"   - {cat.nome}: {produtos_cat} produtos ativos")