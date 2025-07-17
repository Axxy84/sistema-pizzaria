#!/usr/bin/env python
import requests
import json

# Testar diferentes variações da URL
urls_to_test = [
    'http://127.0.0.1:8000/api/pedidos/meio-a-meio/calcular-preco/',
    'http://127.0.0.1:8000/api/pedidos/meio-a-meio/calcular-preco',  # sem trailing slash
    'http://localhost:8000/api/pedidos/meio-a-meio/calcular-preco/',
    'http://127.0.0.1:8080/api/pedidos/meio-a-meio/calcular-preco/',  # porta 8080
    'http://localhost:8080/api/pedidos/meio-a-meio/calcular-preco/',
]

data = {
    'sabor_1_id': 6,
    'sabor_2_id': 5,
    'tamanho_id': 1,
    'regra_preco': 'mais_caro'
}

print("🧪 Testando diferentes URLs...\n")

for url in urls_to_test:
    try:
        response = requests.post(
            url, 
            json=data, 
            timeout=5,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"✅ {url}")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"   Success: {result.get('status', 'unknown')}")
        else:
            print(f"   Error: {response.text[:100]}")
        print()
        
    except requests.exceptions.ConnectionError:
        print(f"❌ {url}")
        print(f"   Connection refused")
        print()
    except Exception as e:
        print(f"💥 {url}")
        print(f"   Error: {str(e)}")
        print()

# Testar portas em uso
print("🔍 Verificando portas em uso...")
import subprocess
try:
    result = subprocess.run(['ss', '-tulpn'], capture_output=True, text=True)
    lines = result.stdout.split('\n')
    for line in lines:
        if ':8000' in line or ':8080' in line:
            print(f"   {line.strip()}")
except:
    print("   Não foi possível verificar portas")