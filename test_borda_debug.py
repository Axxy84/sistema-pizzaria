#!/usr/bin/env python
import requests
import json

# Testar API de produtos
response = requests.get('http://127.0.0.1:8000/api/produtos/produtos/para_pedido/')
data = response.json()

print("=== BORDAS DA API ===")
print(json.dumps(data['bordas'], indent=2))

print("\n=== ESTRUTURA DE UMA BORDA ===")
if data['bordas']:
    primeira_borda = data['bordas'][0]
    print(f"Tipo: {type(primeira_borda)}")
    print(f"Campos: {primeira_borda.keys()}")
    print(f"Dados completos: {json.dumps(primeira_borda, indent=2)}")