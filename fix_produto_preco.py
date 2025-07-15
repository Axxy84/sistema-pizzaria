#!/usr/bin/env python
import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoProject.settings')
django.setup()

from apps.produtos.models import Produto, ProdutoPreco, Tamanho

# Verificar se existem tamanhos
tamanhos = Tamanho.objects.all()
if not tamanhos.exists():
    print("❌ Nenhum tamanho cadastrado. Criando tamanhos padrão...")
    # Criar tamanhos padrão
    Tamanho.objects.create(nome="Único", ordem=1)
    Tamanho.objects.create(nome="Pequeno", ordem=2)
    Tamanho.objects.create(nome="Médio", ordem=3)
    Tamanho.objects.create(nome="Grande", ordem=4)
    print("✅ Tamanhos criados!")

# Buscar tamanho padrão
tamanho_unico = Tamanho.objects.filter(nome="Único").first()
if not tamanho_unico:
    tamanho_unico = Tamanho.objects.first()

print(f"\n🔍 Usando tamanho padrão: {tamanho_unico.nome}")

# Verificar produtos sem ProdutoPreco
produtos = Produto.objects.filter(ativo=True)
print(f'\nTotal de produtos ativos: {produtos.count()}')

produtos_sem_preco = []
for produto in produtos:
    if not ProdutoPreco.objects.filter(produto=produto).exists():
        produtos_sem_preco.append(produto)

print(f'Produtos sem ProdutoPreco: {len(produtos_sem_preco)}')

# Criar ProdutoPreco para produtos que não têm
if produtos_sem_preco:
    print('\n🔧 Criando ProdutoPreco para produtos sem registro...')
    for produto in produtos_sem_preco:
        if produto.preco_unitario:
            produto_preco = ProdutoPreco.objects.create(
                produto=produto,
                tamanho=tamanho_unico,
                preco=produto.preco_unitario
            )
            print(f'✅ Criado ProdutoPreco para: {produto.nome} - R$ {produto.preco_unitario}')
        else:
            print(f'❌ Produto sem preço unitário: {produto.nome}')

print("\n✅ Processo concluído!")

# Verificar novamente
produtos_sem_preco_final = 0
for produto in Produto.objects.filter(ativo=True):
    if not ProdutoPreco.objects.filter(produto=produto).exists():
        produtos_sem_preco_final += 1

print(f'\nVerificação final: {produtos_sem_preco_final} produtos ainda sem ProdutoPreco')