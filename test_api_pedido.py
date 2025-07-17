#!/usr/bin/env python
import requests
import json

# URL do servidor local
BASE_URL = "http://127.0.0.1:8000"

# Dados do pedido de teste
pedido_data = {
    "tipo": "delivery",
    "forma_pagamento": "dinheiro",
    "troco_para": "",
    "observacoes": "",
    "cliente": {
        "nome": "João Silva",
        "telefone": "(11) 98765-4321",
        "endereco": {
            "rua": "Rua das Flores",
            "numero": "123",
            "bairro": "Centro",
            "cidade": "São Paulo",
            "estado": "SP",
            "cep": "01234-567",
            "complemento": ""
        }
    },
    "itens": [
        {
            "produto_id": 1,  # Pizza Margherita
            "quantidade": 2,
            "preco_unitario": 45.00,
            "observacoes": ""
        }
    ],
    "taxa_entrega": 5.00,
    "total": 95.00
}

print("🧪 Testando endpoint criar_pedido_seguro...")
print(f"📦 Dados enviados:\n{json.dumps(pedido_data, indent=2)}")
print("-" * 80)

try:
    # Fazer a requisição
    response = requests.post(
        f"{BASE_URL}/api/pedidos/pedidos/criar_pedido_seguro/",
        json=pedido_data,
        headers={
            "Content-Type": "application/json"
        }
    )
    
    print(f"📡 Status da resposta: {response.status_code}")
    
    # Parse da resposta
    response_data = response.json()
    print(f"📋 Resposta completa:\n{json.dumps(response_data, indent=2, ensure_ascii=False)}")
    
    if response.status_code == 400 and 'erros' in response_data:
        print("\n❌ ERROS DE VALIDAÇÃO ENCONTRADOS:")
        for i, erro in enumerate(response_data['erros'], 1):
            print(f"   {i}. {erro}")
    elif response.status_code == 200 and response_data.get('status') == 'success':
        print("\n✅ PEDIDO CRIADO COM SUCESSO!")
        print(f"   ID do pedido: {response_data.get('pedido', {}).get('id')}")
        
except Exception as e:
    print(f"❌ Erro ao executar teste: {e}")
    import traceback
    traceback.print_exc()