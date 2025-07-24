import os
import django
import requests

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoProject.settings')
django.setup()

from django.test import Client

# Criar cliente de teste
client = Client()

# Fazer login
try:
    user = get_user_model().objects.get(username='admin')
    client.force_login(user)
    print("✓ Login realizado com sucesso")
except User.DoesNotExist:
    print("✗ Usuário admin não encontrado")
    # Criar usuário admin
    user = get_user_model().objects.create_superuser('admin', 'admin@example.com', 'admin123')
    client.force_login(user)
    print("✓ Usuário admin criado e logado")

# Testar acesso à página
response = client.get('/pedidos/rapido/')
print(f"\n✓ Status da página: {response.status_code}")

if response.status_code == 200:
    print("✓ Página acessível com sucesso!")
    
    # Verificar se tem conteúdo esperado
    content = response.content.decode('utf-8')
    if 'Novo Pedido Rápido' in content:
        print("✓ Título da página encontrado")
    if 'buscarProdutos' in content:
        print("✓ Função JavaScript encontrada")
    if 'pedidoRapido()' in content:
        print("✓ Alpine component encontrado")
        
    # Salvar HTML para debug
    with open('debug_pedido_rapido.html', 'w') as f:
        f.write(content)
    print("\n✓ HTML salvo em debug_pedido_rapido.html")
    
elif response.status_code == 302:
    print(f"✗ Redirecionamento para: {response.url}")
else:
    print(f"✗ Erro: {response.status_code}")
    print(f"Conteúdo: {response.content.decode('utf-8')[:200]}...")

# Testar também a API de produtos
response = client.get('/api/produtos/para_pedido/')
print(f"\n✓ API de produtos: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(f"✓ Produtos encontrados: {len(data.get('produtos', []))}")