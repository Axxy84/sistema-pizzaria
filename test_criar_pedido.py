#!/usr/bin/env python
import os
import sys
import django
import json

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoProject.settings')
django.setup()

from apps.pedidos.views import criar_pedido_seguro
from django.test import RequestFactory
from django.contrib.auth.models import User

# Criar dados de teste
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
            "produto_id": 1,  # Assumindo que existe um produto com ID 1
            "quantidade": 2,
            "preco_unitario": 45.00,
            "observacoes": ""
        }
    ],
    "taxa_entrega": 5.00,
    "total": 95.00
}

# Criar request simulado
factory = RequestFactory()
request = factory.post('/api/pedidos/pedidos/criar_pedido_seguro/', 
                      data=json.dumps(pedido_data),
                      content_type='application/json')

# Simular usuário autenticado (se necessário)
request.user = None  # Ou User.objects.first() se precisar de autenticação

# Chamar a view diretamente
print("🧪 Testando endpoint criar_pedido_seguro...")
print(f"📦 Dados enviados: {json.dumps(pedido_data, indent=2)}")
print("-" * 50)

try:
    response = criar_pedido_seguro(request)
    response_data = json.loads(response.content.decode('utf-8'))
    
    print(f"📡 Status da resposta: {response.status_code}")
    print(f"📋 Resposta completa: {json.dumps(response_data, indent=2)}")
    
    if response.status_code == 400 and 'erros' in response_data:
        print("\n❌ ERROS DE VALIDAÇÃO ENCONTRADOS:")
        for i, erro in enumerate(response_data['erros'], 1):
            print(f"   {i}. {erro}")
            
except Exception as e:
    print(f"❌ Erro ao executar teste: {e}")
    import traceback
    traceback.print_exc()