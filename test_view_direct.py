#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoProject.settings')
django.setup()

from django.test import RequestFactory
from apps.pedidos.views import calcular_preco_meio_a_meio
import json

def test_view_directly():
    print("=== TESTE DIRETO DA VIEW ===")
    
    # Criar request factory
    factory = RequestFactory()
    
    # Dados do teste
    data = {
        'sabor_1_id': 6,
        'sabor_2_id': 5,
        'tamanho_id': 1,
        'regra_preco': 'mais_caro'
    }
    
    # Criar request POST
    request = factory.post(
        '/api/pedidos/meio-a-meio/calcular-preco/',
        data=json.dumps(data),
        content_type='application/json'
    )
    
    try:
        # Chamar a view diretamente
        response = calcular_preco_meio_a_meio(request)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Data: {response.data}")
        
        if response.status_code == 200:
            print("✅ View funcionando corretamente!")
        else:
            print(f"❌ View retornou erro: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erro ao chamar view: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_view_directly()