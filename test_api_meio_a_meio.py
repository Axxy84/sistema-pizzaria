#!/usr/bin/env python
"""
Script de teste para a API de cálculo de preço meio a meio
"""
import requests
import json
import sys
from datetime import datetime

# URL base da API
BASE_URL = "http://127.0.0.1:8000"
ENDPOINT = f"{BASE_URL}/api/pedidos/meio-a-meio/calcular-preco/"

# Cores para output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'
BOLD = '\033[1m'

def print_test_header(test_name):
    print(f"\n{BLUE}{BOLD}=== {test_name} ==={RESET}")

def print_result(success, message):
    if success:
        print(f"{GREEN}✓ {message}{RESET}")
    else:
        print(f"{RED}✗ {message}{RESET}")

def print_request_info(data):
    print(f"{YELLOW}Request: {json.dumps(data, indent=2)}{RESET}")

def print_response_info(response):
    try:
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except:
        print(f"Response Text: {response.text}")

def test_valid_request():
    """Teste com dados válidos"""
    print_test_header("TESTE 1: Requisição Válida")
    
    data = {
        "sabor_1_id": 2,  # Calabresa
        "sabor_2_id": 3,  # Portuguesa
        "tamanho_id": 1,  # Pequena
        "regra_preco": "mais_caro"
    }
    
    print_request_info(data)
    
    try:
        response = requests.post(ENDPOINT, json=data)
        print_response_info(response)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('status') == 'success':
                preco_final = result['dados']['preco_final']
                print_result(True, f"Preço calculado com sucesso: R$ {preco_final}")
                return True
            else:
                print_result(False, f"Erro na resposta: {result.get('message', 'Desconhecido')}")
        else:
            print_result(False, f"Status HTTP inesperado: {response.status_code}")
    except Exception as e:
        print_result(False, f"Erro na requisição: {str(e)}")
        return False

def test_media_pricing():
    """Teste com regra de média"""
    print_test_header("TESTE 2: Regra de Preço - Média")
    
    data = {
        "sabor_1_id": 2,  # Calabresa (R$ 28)
        "sabor_2_id": 4,  # Quatro Queijos
        "tamanho_id": 1,  # Pequena
        "regra_preco": "media"
    }
    
    print_request_info(data)
    
    try:
        response = requests.post(ENDPOINT, json=data)
        print_response_info(response)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('status') == 'success':
                preco_final = result['dados']['preco_final']
                economia = result['dados']['economia']
                print_result(True, f"Preço médio calculado: R$ {preco_final} (economia: R$ {economia})")
                return True
        else:
            print_result(False, f"Status HTTP: {response.status_code}")
    except Exception as e:
        print_result(False, f"Erro: {str(e)}")
        return False

def test_same_flavor():
    """Teste com sabores iguais (deve falhar)"""
    print_test_header("TESTE 3: Sabores Iguais (Deve Falhar)")
    
    data = {
        "sabor_1_id": 2,  # Calabresa
        "sabor_2_id": 2,  # Calabresa também
        "tamanho_id": 1,
        "regra_preco": "mais_caro"
    }
    
    print_request_info(data)
    
    try:
        response = requests.post(ENDPOINT, json=data)
        print_response_info(response)
        
        if response.status_code == 400:
            result = response.json()
            if "devem ser diferentes" in result.get('message', ''):
                print_result(True, "Validação correta: sabores iguais rejeitados")
                return True
        print_result(False, "Validação falhou - aceitou sabores iguais")
    except Exception as e:
        print_result(False, f"Erro: {str(e)}")
        return False

def test_missing_parameters():
    """Teste com parâmetros faltando"""
    print_test_header("TESTE 4: Parâmetros Faltando")
    
    data = {
        "sabor_1_id": 2,
        # sabor_2_id faltando
        "tamanho_id": 1
    }
    
    print_request_info(data)
    
    try:
        response = requests.post(ENDPOINT, json=data)
        print_response_info(response)
        
        if response.status_code == 400:
            result = response.json()
            if "obrigatórios" in result.get('message', ''):
                print_result(True, "Validação correta: parâmetros obrigatórios verificados")
                return True
        print_result(False, "Validação falhou - aceitou request incompleto")
    except Exception as e:
        print_result(False, f"Erro: {str(e)}")
        return False

def test_invalid_product():
    """Teste com ID de produto inválido"""
    print_test_header("TESTE 5: Produto Inválido")
    
    data = {
        "sabor_1_id": 2,
        "sabor_2_id": 9999,  # ID que não existe
        "tamanho_id": 1,
        "regra_preco": "mais_caro"
    }
    
    print_request_info(data)
    
    try:
        response = requests.post(ENDPOINT, json=data)
        print_response_info(response)
        
        if response.status_code == 404:
            result = response.json()
            if "não foi encontrado" in result.get('message', ''):
                print_result(True, "Validação correta: produto inexistente detectado")
                return True
        print_result(False, "Validação falhou - não detectou produto inválido")
    except Exception as e:
        print_result(False, f"Erro: {str(e)}")
        return False

def test_non_pizza_product():
    """Teste com produto que não é pizza"""
    print_test_header("TESTE 6: Produto Não-Pizza")
    
    # Primeiro vamos tentar descobrir um ID de bebida
    print("Buscando um produto não-pizza para teste...")
    
    data = {
        "sabor_1_id": 2,  # Calabresa (pizza)
        "sabor_2_id": 7,  # Tentativa com ID 7 (pode ser bebida)
        "tamanho_id": 1,
        "regra_preco": "mais_caro"
    }
    
    print_request_info(data)
    
    try:
        response = requests.post(ENDPOINT, json=data)
        print_response_info(response)
        
        if response.status_code in [404, 400]:
            result = response.json()
            if "não é uma pizza" in result.get('message', '') or "não foi encontrado" in result.get('message', ''):
                print_result(True, "Validação correta: produto não-pizza rejeitado")
                return True
        print_result(False, "Validação pode ter falhado")
    except Exception as e:
        print_result(False, f"Erro: {str(e)}")
        return False

def test_different_sizes():
    """Teste com diferentes tamanhos"""
    print_test_header("TESTE 7: Diferentes Tamanhos")
    
    tamanhos = [
        (1, "Pequena"),
        (2, "Média"),
        (3, "Grande"),
        (4, "Família")
    ]
    
    for tamanho_id, tamanho_nome in tamanhos:
        print(f"\n{BOLD}Testando tamanho: {tamanho_nome}{RESET}")
        
        data = {
            "sabor_1_id": 2,  # Calabresa
            "sabor_2_id": 3,  # Portuguesa
            "tamanho_id": tamanho_id,
            "regra_preco": "mais_caro"
        }
        
        try:
            response = requests.post(ENDPOINT, json=data)
            if response.status_code == 200:
                result = response.json()
                preco = result['dados']['preco_final']
                print(f"  {GREEN}✓ {tamanho_nome}: R$ {preco}{RESET}")
            else:
                print(f"  {RED}✗ {tamanho_nome}: Erro {response.status_code}{RESET}")
        except Exception as e:
            print(f"  {RED}✗ {tamanho_nome}: {str(e)}{RESET}")
    
    return True

def test_price_no_configuration():
    """Teste com tamanho sem preço configurado"""
    print_test_header("TESTE 8: Tamanho Sem Preço Configurado")
    
    data = {
        "sabor_1_id": 2,  # Calabresa
        "sabor_2_id": 3,  # Portuguesa
        "tamanho_id": 5,  # Broto (pode não ter preço configurado)
        "regra_preco": "mais_caro"
    }
    
    print_request_info(data)
    
    try:
        response = requests.post(ENDPOINT, json=data)
        print_response_info(response)
        
        if response.status_code == 404:
            result = response.json()
            if "Preço não encontrado" in result.get('message', ''):
                print_result(True, "Validação correta: detectou falta de preço")
                return True
        elif response.status_code == 200:
            print_result(True, "Tamanho tem preço configurado - OK")
            return True
        else:
            print_result(False, f"Resposta inesperada: {response.status_code}")
    except Exception as e:
        print_result(False, f"Erro: {str(e)}")
        return False

def main():
    print(f"{BOLD}{'='*60}")
    print(f"TESTE DA API DE CÁLCULO DE PREÇO MEIO A MEIO")
    print(f"Endpoint: {ENDPOINT}")
    print(f"Data/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}{RESET}")
    
    # Verificar se o servidor está rodando
    try:
        response = requests.get(BASE_URL)
        print(f"{GREEN}✓ Servidor Django está rodando{RESET}")
    except:
        print(f"{RED}✗ Erro: Servidor não está rodando em {BASE_URL}{RESET}")
        print(f"{YELLOW}Execute 'python manage.py runserver' primeiro{RESET}")
        sys.exit(1)
    
    # Executar todos os testes
    tests = [
        test_valid_request,
        test_media_pricing,
        test_same_flavor,
        test_missing_parameters,
        test_invalid_product,
        test_non_pizza_product,
        test_different_sizes,
        test_price_no_configuration
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"{RED}Erro no teste: {str(e)}{RESET}")
            failed += 1
    
    # Resumo final
    print(f"\n{BOLD}{'='*60}")
    print(f"RESUMO DOS TESTES")
    print(f"{'='*60}{RESET}")
    print(f"{GREEN}Testes aprovados: {passed}{RESET}")
    print(f"{RED}Testes falhados: {failed}{RESET}")
    print(f"Total: {passed + failed}")
    
    if failed == 0:
        print(f"\n{GREEN}{BOLD}✓ TODOS OS TESTES PASSARAM!{RESET}")
    else:
        print(f"\n{RED}{BOLD}✗ ALGUNS TESTES FALHARAM{RESET}")

if __name__ == "__main__":
    main()