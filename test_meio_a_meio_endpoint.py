#!/usr/bin/env python
import os
import sys
import django
import requests
from django.test import Client

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoProject.settings')
django.setup()

from apps.produtos.models import Produto

# Test using requests library
def test_with_requests():
    print("=== Testing meio-a-meio endpoint with requests ===")
    
    # Get some pizza IDs
    pizzas = Produto.objects.filter(categoria__nome__icontains='pizza').values('id', 'nome')[:2]
    if len(pizzas) < 2:
        print("❌ Need at least 2 pizzas to test")
        return
    
    # Assume tamanho_id 1 exists (you may need to adjust)
    data = {
        'sabor_1_id': pizzas[0]['id'],
        'sabor_2_id': pizzas[1]['id'],
        'tamanho_id': 1,
        'regra_preco': 'mais_caro'
    }
    
    print(f"Testing with pizzas: {pizzas[0]['nome']} + {pizzas[1]['nome']}")
    
    # Test both ports
    for port in [8000, 8080]:
        url = f'http://127.0.0.1:{port}/api/pedidos/meio-a-meio/calcular-preco/'
        try:
            response = requests.post(url, json=data)
            print(f"\nPort {port}:")
            print(f"  Status: {response.status_code}")
            if response.status_code == 200:
                print(f"  Response: {response.json()}")
            else:
                print(f"  Error: {response.text}")
        except requests.exceptions.ConnectionError:
            print(f"\nPort {port}: Connection refused (server not running)")

# Test using Django test client
def test_with_django_client():
    print("\n=== Testing meio-a-meio endpoint with Django test client ===")
    
    client = Client()
    
    # Get some pizza IDs
    pizzas = Produto.objects.filter(categoria__nome__icontains='pizza').values('id', 'nome')[:2]
    if len(pizzas) < 2:
        print("❌ Need at least 2 pizzas to test")
        return
    
    data = {
        'sabor_1_id': pizzas[0]['id'],
        'sabor_2_id': pizzas[1]['id'],
        'tamanho_id': 1,
        'regra_preco': 'mais_caro'
    }
    
    print(f"Testing with pizzas: {pizzas[0]['nome']} + {pizzas[1]['nome']}")
    
    # Test the endpoint
    response = client.post(
        '/api/pedidos/meio-a-meio/calcular-preco/',
        data=data,
        content_type='application/json'
    )
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print(f"Response: {response.json()}")
    else:
        print(f"Error: {response.content.decode()}")

if __name__ == "__main__":
    try:
        import requests
        test_with_requests()
    except ImportError:
        print("requests library not installed, skipping requests test")
    
    test_with_django_client()