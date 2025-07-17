import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoProject.settings')
django.setup()

from apps.produtos.models import Tamanho, ProdutoPreco, Produto
from django.db import transaction

print("=== REMOVENDO 'BROTO' DO SISTEMA ===\n")

# 1. Verificar tamanho Broto
tamanho_broto = Tamanho.objects.filter(nome='Broto').first()
if not tamanho_broto:
    print("✓ Tamanho 'Broto' não encontrado no sistema")
    exit()

print(f"Encontrado tamanho 'Broto' (ID: {tamanho_broto.id})")

# 2. Verificar produtos usando Broto
produtos_com_broto = ProdutoPreco.objects.filter(tamanho=tamanho_broto).select_related('produto', 'produto__categoria')
total = produtos_com_broto.count()
print(f"\n📊 {total} produtos usando tamanho 'Broto':")

# Agrupar por categoria
por_categoria = {}
for pp in produtos_com_broto:
    cat = pp.produto.categoria.nome if pp.produto.categoria else 'Sem categoria'
    if cat not in por_categoria:
        por_categoria[cat] = []
    por_categoria[cat].append(pp.produto.nome)

for cat, produtos in por_categoria.items():
    print(f"\n{cat}: {len(produtos)} produtos")
    for p in produtos[:5]:
        print(f"  - {p}")
    if len(produtos) > 5:
        print(f"  ... e mais {len(produtos) - 5}")

# 3. Criar ou buscar tamanho "Único"
tamanho_unico = Tamanho.objects.filter(nome='Único').first()
if not tamanho_unico:
    print("\n✓ Criando tamanho 'Único'...")
    tamanho_unico = Tamanho.objects.create(
        nome='Único',
        ordem=0,
        ativo=True
    )

# 4. Executar remoção
print("\n🔄 Iniciando processo de remoção...")

with transaction.atomic():
    # Atualizar produtos que não são pizzas para usar "Único"
    bebidas_atualizadas = ProdutoPreco.objects.filter(
        tamanho=tamanho_broto,
        produto__categoria__nome='Bebidas'
    ).update(tamanho=tamanho_unico)
    print(f"✓ {bebidas_atualizadas} bebidas atualizadas para 'Único'")
    
    bordas_atualizadas = ProdutoPreco.objects.filter(
        tamanho=tamanho_broto,
        produto__categoria__nome='Bordas Recheadas'
    ).update(tamanho=tamanho_unico)
    print(f"✓ {bordas_atualizadas} bordas atualizadas para 'Único'")
    
    sobremesas_atualizadas = ProdutoPreco.objects.filter(
        tamanho=tamanho_broto,
        produto__categoria__nome='Sobremesas'
    ).update(tamanho=tamanho_unico)
    print(f"✓ {sobremesas_atualizadas} sobremesas atualizadas para 'Único'")
    
    # Para pizzas com Broto, vamos deletar pois pizzas devem ter P, M, G
    pizzas_broto = ProdutoPreco.objects.filter(
        tamanho=tamanho_broto,
        produto__categoria__nome__icontains='Pizza'
    )
    pizzas_deletadas = pizzas_broto.count()
    pizzas_broto.delete()
    print(f"✓ {pizzas_deletadas} preços de pizza com 'Broto' removidos")
    
    # Remover o tamanho Broto
    tamanho_broto.delete()
    print(f"✓ Tamanho 'Broto' removido do sistema")

print("\n✅ PROCESSO CONCLUÍDO!")

# Verificar resultado
print("\n📋 VERIFICAÇÃO FINAL:")
tamanhos = Tamanho.objects.filter(ativo=True).order_by('ordem')
print("\nTamanhos disponíveis:")
for t in tamanhos:
    count = ProdutoPreco.objects.filter(tamanho=t).count()
    print(f"  - {t.nome}: {count} produtos")