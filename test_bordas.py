#!/usr/bin/env python
import os
import sys
import django

# Configurar Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoProject.settings')
django.setup()

from apps.produtos.models import Produto, Categoria

# Verificar bordas
print("=== VERIFICANDO BORDAS NO BANCO ===")

# Buscar categorias que possam conter bordas
categorias_borda = Categoria.objects.filter(nome__icontains='borda')
print(f"\nCategorias com 'borda' no nome: {categorias_borda.count()}")
for cat in categorias_borda:
    print(f"- {cat.nome} (ID: {cat.id})")

# Buscar produtos que possam ser bordas
produtos_borda = Produto.objects.filter(nome__icontains='borda')
print(f"\nProdutos com 'borda' no nome: {produtos_borda.count()}")
for prod in produtos_borda:
    print(f"- {prod.nome} - Categoria: {prod.categoria.nome if prod.categoria else 'Sem categoria'} - Preço: R$ {prod.preco_unitario}")

# Verificar também por categoria adicional
produtos_adicional = Produto.objects.filter(categoria__nome__icontains='adicional')
print(f"\nProdutos em categoria 'adicional': {produtos_adicional.count()}")
for prod in produtos_adicional:
    print(f"- {prod.nome} - Preço: R$ {prod.preco_unitario}")

# Listar todas as categorias
print("\n=== TODAS AS CATEGORIAS ===")
for cat in Categoria.objects.all():
    print(f"- {cat.nome} ({Produto.objects.filter(categoria=cat).count()} produtos)")