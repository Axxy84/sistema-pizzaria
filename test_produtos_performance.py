#!/usr/bin/env python
"""
Script para testar a performance do carregamento de produtos
"""
import os
import django
import sys
import time
import requests

# Adiciona o diretório do projeto ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Configura o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoProject.settings')
django.setup()

from django.core.cache import cache
from django.test import Client
from apps.produtos.models import Produto

def test_performance():
    """Testa a performance dos endpoints de produtos"""
    print("=== Teste de Performance de Produtos ===\n")
    
    # Limpar cache para teste justo
    cache.clear()
    print("✓ Cache limpo\n")
    
    # Endpoints para testar
    endpoints = [
        '/api/produtos/produtos/para_pedido/',
        '/api/produtos/produtos/para_pedido_rapido/',
        '/produtos/',
    ]
    
    # Cliente de teste
    client = Client()
    
    # Login
    user = get_user_model().objects.first()
    if user:
        client.force_login(user)
    
    # Testar cada endpoint
    for endpoint in endpoints:
        print(f"\n--- Testando: {endpoint} ---")
        
        # Primeira requisição (sem cache)
        start = time.time()
        response = client.get(endpoint)
        first_time = time.time() - start
        
        print(f"✓ Primeira requisição: {first_time:.3f}s")
        print(f"  Status: {response.status_code}")
        
        if response.status_code == 200:
            if 'application/json' in response.get('Content-Type', ''):
                try:
                    data = response.json()
                    if isinstance(data, dict):
                        total_items = sum(len(v) if isinstance(v, list) else 0 for v in data.values())
                        print(f"  Produtos retornados: {total_items}")
                    elif isinstance(data, list):
                        print(f"  Produtos retornados: {len(data)}")
                except:
                    pass
        
        # Segunda requisição (com cache)
        start = time.time()
        response = client.get(endpoint)
        second_time = time.time() - start
        
        print(f"✓ Segunda requisição: {second_time:.3f}s")
        
        # Calcular melhoria
        if first_time > 0:
            improvement = ((first_time - second_time) / first_time) * 100
            print(f"  Melhoria: {improvement:.1f}%")
    
    # Estatísticas do banco
    print(f"\n--- Estatísticas do Banco ---")
    print(f"Total de produtos: {Produto.objects.count()}")
    print(f"Produtos ativos: {Produto.objects.filter(ativo=True).count()}")
    
    # Verificar cache
    print(f"\n--- Status do Cache ---")
    cache_key = 'produtos:para_pedido:v2'
    cached_data = cache.get(cache_key)
    if cached_data:
        print(f"✓ Cache ativo para produtos")
        print(f"  Categorias no cache: {list(cached_data.keys())}")
    else:
        print("✗ Cache vazio")

if __name__ == "__main__":
    test_performance()