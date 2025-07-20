#!/usr/bin/env python
"""
Script para testar a página de pedidos diretamente
"""
import os
import django
import sys

# Adiciona o diretório do projeto ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Configura o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoProject.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User

def test_pedidos_page():
    """Testa o acesso à página de pedidos"""
    print("=== Teste da Página de Pedidos ===\n")
    
    # Cria um cliente de teste
    client = Client()
    
    # Tenta acessar sem login
    print("1. Testando acesso sem login...")
    response = client.get('/pedidos/')
    print(f"   Status: {response.status_code}")
    if response.status_code == 302:
        print(f"   Redirecionado para: {response.url}")
    
    # Faz login
    print("\n2. Fazendo login...")
    user = User.objects.filter(username='Axxycorporation@gmail.com').first()
    if user:
        client.force_login(user)
        print(f"   Login realizado: {user.username}")
    else:
        print("   ERRO: Usuário não encontrado!")
        return
    
    # Tenta acessar com login
    print("\n3. Testando acesso com login...")
    response = client.get('/pedidos/')
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        print("   ✅ Página carregada com sucesso!")
        # Verifica conteúdo básico
        content = response.content.decode('utf-8')
        if 'Pedidos' in content:
            print("   ✅ Título 'Pedidos' encontrado")
        if 'pedido_list' in content or 'pedidos' in content:
            print("   ✅ Lista de pedidos presente")
    else:
        print(f"   ❌ Erro ao carregar página")
        if response.status_code == 302:
            print(f"   Redirecionado para: {response.url}")

if __name__ == "__main__":
    test_pedidos_page()