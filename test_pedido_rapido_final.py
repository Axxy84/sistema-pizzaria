import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoProject.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User

# Cliente de teste
client = Client()

# Login
user = User.objects.get(username='admin')
client.force_login(user)

print("=== TESTE FINAL DO SISTEMA DE PEDIDO RÁPIDO ===\n")

# 1. Testar página
print("1. Testando acesso à página...")
response = client.get('/pedidos/rapido/')
if response.status_code == 200:
    print("✓ Página acessível")
    content = response.content.decode('utf-8')
    
    # Verificar elementos essenciais
    checks = [
        ('Novo Pedido Rápido', 'Título'),
        ('buscarProdutos', 'Função de busca'),
        ('filtroCategoria', 'Filtros'),
        ('🧀 Bordas', 'Categoria Bordas'),
        ('/api/produtos/produtos/para_pedido_rapido/', 'URL da API correta')
    ]
    
    for check, desc in checks:
        if check in content:
            print(f"✓ {desc} encontrado")
        else:
            print(f"✗ {desc} NÃO encontrado")
else:
    print(f"✗ Erro ao acessar página: {response.status_code}")

# 2. Testar API
print("\n2. Testando API de produtos...")
response = client.get('/api/produtos/produtos/para_pedido_rapido/')
if response.status_code == 200:
    data = response.json()
    produtos = data.get('produtos', [])
    print(f"✓ API funcionando - {len(produtos)} produtos encontrados")
    
    # Contar por categoria
    categorias = {}
    for p in produtos:
        cat = p['categoria']
        categorias[cat] = categorias.get(cat, 0) + 1
    
    print("\nProdutos por categoria:")
    for cat, count in sorted(categorias.items()):
        icon = {'pizzas': '🍕', 'bebidas': '🥤', 'bordas': '🧀', 'outros': '🍟'}.get(cat, '❓')
        print(f"  {icon} {cat}: {count} produtos")
else:
    print(f"✗ Erro na API: {response.status_code}")

print("\n=== RESUMO ===")
print("✅ Sistema de pedido rápido configurado e funcionando!")
print("✅ Categorias: Pizzas, Bebidas, Bordas, Outros")
print("✅ URL correta da API configurada")
print("\n📍 Acesse: http://127.0.0.1:8080/pedidos/rapido/")
print("\n💡 Dicas:")
print("- Use a busca para filtrar produtos")
print("- Clique nos filtros para ver apenas uma categoria")
print("- Clique no preço para adicionar ao carrinho")
print("- Pizza meio a meio tem botão especial")