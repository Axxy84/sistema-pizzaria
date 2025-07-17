import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoProject.settings')
django.setup()

from apps.produtos.models import ProdutoPreco, Tamanho

# Verificar tamanhos
print("=== VERIFICANDO TAMANHOS ===")
for pp in ProdutoPreco.objects.select_related('produto', 'tamanho', 'produto__categoria'):
    if pp.produto.categoria and pp.produto.categoria.nome in ['Bebidas', 'Bordas Recheadas']:
        print(f"{pp.produto.categoria.nome}: {pp.produto.nome} - Tamanho: {pp.tamanho.nome if pp.tamanho else 'SEM TAMANHO'}")

# Verificar se existe tamanho "Único"
tamanho_unico = Tamanho.objects.filter(nome='Único').first()
if not tamanho_unico:
    print("\n⚠️  Tamanho 'Único' não existe. Criando...")
    tamanho_unico = Tamanho.objects.create(
        nome='Único',
        descricao='Tamanho único',
        ordem=0,
        ativo=True
    )
    print("✓ Tamanho 'Único' criado")

# Contar produtos afetados
bebidas_broto = ProdutoPreco.objects.filter(
    produto__categoria__nome='Bebidas',
    tamanho__nome='Broto'
).count()

bordas_broto = ProdutoPreco.objects.filter(
    produto__categoria__nome='Bordas Recheadas',
    tamanho__nome='Broto'
).count()

print(f"\n📊 Produtos com tamanho incorreto:")
print(f"- Bebidas com 'Broto': {bebidas_broto}")
print(f"- Bordas com 'Broto': {bordas_broto}")

# Perguntar se quer corrigir
if bebidas_broto > 0 or bordas_broto > 0:
    resposta = input("\nDeseja corrigir os tamanhos? (s/n): ")
    if resposta.lower() == 's':
        # Corrigir bebidas
        updated = ProdutoPreco.objects.filter(
            produto__categoria__nome='Bebidas',
            tamanho__nome='Broto'
        ).update(tamanho=tamanho_unico)
        print(f"✓ {updated} bebidas corrigidas")
        
        # Corrigir bordas
        updated = ProdutoPreco.objects.filter(
            produto__categoria__nome='Bordas Recheadas',
            tamanho__nome='Broto'
        ).update(tamanho=tamanho_unico)
        print(f"✓ {updated} bordas corrigidas")
        
        print("\n✅ Tamanhos corrigidos com sucesso!")