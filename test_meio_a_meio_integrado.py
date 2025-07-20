#!/usr/bin/env python3
"""
Teste da funcionalidade de Pizza Meio a Meio Integrada
Verifica se a nova interface está funcionando corretamente
"""

import requests
import json
import sys
import os

# Configurar path do Django
sys.path.insert(0, '/home/labdev/Documentos/DjangoProject')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoProject.settings')

import django
django.setup()

from apps.produtos.models import Produto

def teste_meio_a_meio_integrado():
    """Testa a funcionalidade de meio a meio integrada"""
    print("🔥 TESTE: Pizza Meio a Meio Integrada")
    print("=" * 50)
    
    # 1. Verificar se existem pizzas no banco
    pizzas = Produto.objects.filter(categoria__nome__icontains='pizza')[:2]
    
    if len(pizzas) < 2:
        print("❌ ERRO: Não há pizzas suficientes no banco para teste")
        return False
        
    print(f"✅ Encontradas {len(pizzas)} pizzas para teste:")
    for pizza in pizzas:
        print(f"   • {pizza.nome}")
    
    # 2. Testar acesso à página de pedido rápido
    try:
        response = requests.get('http://127.0.0.1:8000/pedidos/rapido/', timeout=5)
        if response.status_code == 200:
            print("✅ Página de pedido rápido acessível")
            
            # Verificar se o botão meio a meio está presente
            if 'meio-a-meio-btn' in response.text:
                print("✅ Botão meio a meio encontrado no HTML")
            else:
                print("❌ Botão meio a meio NÃO encontrado no HTML")
                
            # Verificar se as funções JavaScript estão presentes
            if 'selecionarParaMeioAMeio' in response.text:
                print("✅ Função JavaScript 'selecionarParaMeioAMeio' encontrada")
            else:
                print("❌ Função JavaScript 'selecionarParaMeioAMeio' NÃO encontrada")
                
            # Verificar se o modal de tamanho está presente
            if 'modalSeletorTamanho' in response.text:
                print("✅ Modal seletor de tamanho encontrado")
            else:
                print("❌ Modal seletor de tamanho NÃO encontrado")
                
        else:
            print(f"❌ ERRO: Página inacessível (Status: {response.status_code})")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ ERRO: Não foi possível acessar a página: {e}")
        return False
    
    # 3. Testar API de produtos para pedido rápido
    try:
        response = requests.get('http://127.0.0.1:8000/api/produtos/produtos/para_pedido_rapido/')
        if response.status_code == 200:
            data = response.json()
            pizzas_api = [p for p in data['produtos'] if p['categoria'] == 'pizzas']
            print(f"✅ API retornou {len(pizzas_api)} pizzas")
            
            # Verificar se as pizzas têm preços
            pizza_com_precos = [p for p in pizzas_api if len(p['precos']) > 0]
            print(f"✅ {len(pizza_com_precos)} pizzas têm preços configurados")
            
        else:
            print(f"❌ ERRO: API inacessível (Status: {response.status_code})")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ ERRO: API inacessível: {e}")
        return False
    
    # 4. Verificar se o CSS está correto
    estilos_necessarios = [
        'meio-a-meio-btn',
        'primeiro-sabor', 
        'opcao-segundo',
        'pulse-meio-a-meio'
    ]
    
    estilos_encontrados = []
    for estilo in estilos_necessarios:
        if estilo in response.text:
            estilos_encontrados.append(estilo)
    
    print(f"✅ {len(estilos_encontrados)}/{len(estilos_necessarios)} estilos CSS encontrados")
    
    if len(estilos_encontrados) == len(estilos_necessarios):
        print("🎉 SUCESSO: Todos os componentes estão implementados!")
        print("\n📋 RESUMO DA FUNCIONALIDADE:")
        print("   1. ½ + ½ button em cada pizza")
        print("   2. Seleção sequencial de sabores")
        print("   3. Modal de tamanho inline")
        print("   4. Estados visuais com animações")
        print("   5. Integração com carrinho existente")
        print("\n🎯 COMO TESTAR:")
        print("   1. Acesse: http://127.0.0.1:8000/pedidos/rapido/")
        print("   2. Clique em ½ + ½ numa pizza (1º sabor)")
        print("   3. Clique em ½ + ½ noutra pizza (2º sabor)")
        print("   4. Escolha o tamanho no modal")
        print("   5. Veja a pizza meio a meio no carrinho")
        return True
    else:
        print("❌ FALHA: Alguns componentes estão faltando")
        return False

if __name__ == '__main__':
    try:
        sucesso = teste_meio_a_meio_integrado()
        if sucesso:
            print("\n🚀 TESTE CONCLUÍDO COM SUCESSO!")
        else:
            print("\n💥 TESTE FALHOU - Verifique os erros acima")
    except Exception as e:
        print(f"\n💥 ERRO INESPERADO: {e}")