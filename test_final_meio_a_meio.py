#!/usr/bin/env python
"""
Teste final da funcionalidade meio a meio
"""

import requests
import json

def test_meio_a_meio_completo():
    print("🧪 TESTE FINAL DA FUNCIONALIDADE MEIO A MEIO")
    print("=" * 50)
    
    base_url = "http://127.0.0.1:8000"
    
    # 1. Teste da API de sabores
    print("\n1. 🍕 Testando API de sabores disponíveis...")
    try:
        response = requests.get(f"{base_url}/api/pedidos/meio-a-meio/sabores/")
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'success':
                print(f"   ✅ {data['total']} sabores disponíveis")
                sabores = data['sabores'][:2]  # Pegar 2 primeiros
                print(f"   📋 Testando com: {sabores[0]['nome']} + {sabores[1]['nome']}")
            else:
                print(f"   ❌ Erro na API: {data}")
                return False
        else:
            print(f"   ❌ Erro HTTP: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Erro de conexão: {e}")
        return False
    
    # 2. Teste do cálculo de preço
    print("\n2. 💰 Testando cálculo de preço...")
    try:
        payload = {
            "sabor_1_id": sabores[0]['id'],
            "sabor_2_id": sabores[1]['id'], 
            "tamanho_id": 1,  # ID do tamanho "Pequena"
            "regra_preco": "mais_caro"
        }
        
        response = requests.post(
            f"{base_url}/api/pedidos/meio-a-meio/calcular-preco/",
            json=payload,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'success':
                preco = data['dados']['preco_final']
                economia = data['dados']['economia']
                print(f"   ✅ Preço calculado: R$ {preco}")
                print(f"   💡 Economia com média: R$ {economia}")
            else:
                print(f"   ❌ Erro no cálculo: {data.get('message', 'Erro desconhecido')}")
                return False
        else:
            print(f"   ❌ Erro HTTP: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Erro de conexão: {e}")
        return False
    
    # 3. Teste da interface web
    print("\n3. 🌐 Testando interface web...")
    try:
        # Fazer login
        session = requests.Session()
        session.get(f"{base_url}/force-login/")
        
        # Acessar página de pedidos
        response = session.get(f"{base_url}/pedidos/novo/")
        
        if response.status_code == 200:
            html = response.text
            
            # Verificar se elementos meio a meio estão presentes
            checks = [
                ("modalMeioAMeioMostrar", "Variável do modal"),
                ("abrirModalMeioAMeio", "Função de abertura"),
                ("PERSONALIZAR", "Botão personalizar"),
                ("MEIO & MEIO", "Texto meio a meio"),
                ("pedidos-simples.js", "JavaScript carregado")
            ]
            
            all_ok = True
            for check, desc in checks:
                if check in html:
                    print(f"   ✅ {desc} presente")
                else:
                    print(f"   ❌ {desc} ausente")
                    all_ok = False
            
            if not all_ok:
                return False
                
        else:
            print(f"   ❌ Erro ao acessar página: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Erro de conexão: {e}")
        return False
    
    # 4. Resumo final
    print("\n" + "=" * 50)
    print("🎉 TODOS OS TESTES PASSARAM!")
    print("\n📋 Funcionalidades verificadas:")
    print("   ✅ API de sabores disponíveis")
    print("   ✅ Cálculo de preço meio a meio")
    print("   ✅ Interface web carregando")
    print("   ✅ JavaScript configurado")
    print("   ✅ Modal meio a meio presente")
    
    print(f"\n🔗 Acesse: {base_url}/pedidos/novo/")
    print("   1. Clique no botão laranja '🍕 Personalizar'")
    print("   2. Selecione dois sabores diferentes")
    print("   3. Escolha um tamanho")
    print("   4. Veja o preço sendo calculado")
    print("   5. Adicione ao carrinho")
    
    return True

if __name__ == '__main__':
    test_meio_a_meio_completo()