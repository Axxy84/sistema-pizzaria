#!/usr/bin/env python
import os
import sys
from decimal import Decimal
from datetime import datetime

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoProject.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import django
django.setup()

from django.utils import timezone
from apps.clientes.models import Cliente, Endereco
from apps.financeiro.models import Caixa
from apps.pedidos.models_mesa import Mesa

print("=== CONFIGURANDO DADOS INICIAIS ===\n")

# 1. Criar algumas mesas
print("📍 Criando mesas...")
mesas_criadas = []
for i in range(1, 11):  # Criar 10 mesas
    mesa, created = Mesa.objects.get_or_create(
        numero=str(i),
        defaults={
            'status': 'fechada',
            'responsavel': 'Sistema'
        }
    )
    if created:
        mesas_criadas.append(i)

print(f"  ✅ {len(mesas_criadas)} mesas criadas (1-10)")

# 2. Criar alguns clientes de exemplo
print("\n👥 Criando clientes de exemplo...")
clientes_data = [
    {
        'nome': 'Cliente Balcão',
        'telefone': '(11) 99999-0001',
        'email': 'balcao@pizzaria.com',
        'cpf': '111.111.111-11',
        'tipo': 'balcao'
    },
    {
        'nome': 'João Silva',
        'telefone': '(11) 98765-4321',
        'email': 'joao@email.com',
        'cpf': '123.456.789-10',
        'tipo': 'delivery',
        'endereco': {
            'cep': '01310-100',
            'logradouro': 'Av. Paulista',
            'numero': '1000',
            'complemento': 'Apto 101',
            'bairro': 'Bela Vista',
            'cidade': 'São Paulo',
            'estado': 'SP',
            'referencia': 'Próximo ao metrô'
        }
    },
    {
        'nome': 'Maria Santos',
        'telefone': '(11) 91234-5678',
        'email': 'maria@email.com',
        'cpf': '987.654.321-00',
        'tipo': 'delivery',
        'endereco': {
            'cep': '04567-000',
            'logradouro': 'Rua das Flores',
            'numero': '123',
            'bairro': 'Jardim',
            'cidade': 'São Paulo',
            'estado': 'SP'
        }
    }
]

clientes_criados = 0
for cliente_data in clientes_data:
    endereco_data = cliente_data.pop('endereco', None)
    tipo = cliente_data.pop('tipo', 'balcao')
    
    cliente, created = Cliente.objects.get_or_create(
        telefone=cliente_data['telefone'],
        defaults=cliente_data
    )
    
    if created:
        clientes_criados += 1
        print(f"  ✅ Cliente '{cliente.nome}' criado")
        
        # Criar endereço se fornecido
        if endereco_data and tipo == 'delivery':
            endereco = Endereco.objects.create(
                cliente=cliente,
                **endereco_data
            )
            print(f"     📍 Endereço adicionado")

print(f"\nTotal: {clientes_criados} clientes criados")

# 3. Abrir o caixa do dia
print("\n💰 Configurando caixa...")

# Buscar usuário admin
admin_user = get_user_model().objects.filter(is_superuser=True).first()
if not admin_user:
    admin_user = get_user_model().objects.first()

# Verificar se já existe caixa aberto
caixa_aberto = Caixa.objects.filter(status='aberto').first()

if not caixa_aberto:
    # Criar novo caixa
    caixa = Caixa.objects.create(
        usuario=admin_user,
        valor_abertura=Decimal('100.00'),
        status='aberto',
        observacoes_abertura='Caixa aberto pelo sistema de setup inicial'
    )
    print(f"  ✅ Novo caixa aberto com saldo inicial de R$ 100,00")
else:
    print(f"  ℹ️  Já existe um caixa aberto (ID: {caixa_aberto.id})")
    caixa = caixa_aberto

# 4. Mostrar resumo
print("\n📊 RESUMO DO SISTEMA:")
print(f"  Mesas disponíveis: {Mesa.objects.count()}")
print(f"  Clientes cadastrados: {Cliente.objects.count()}")
print(f"  Endereços cadastrados: {Endereco.objects.count()}")
print(f"  Caixa: {'ABERTO' if caixa.status == 'aberto' else 'FECHADO'}")

print("\n🎯 Sistema configurado e pronto para uso!")
print("\n💡 Dicas:")
print("- Para criar pedido de MESA: Selecione tipo 'Mesa' e escolha o número")
print("- Para criar pedido BALCÃO: Selecione tipo 'Balcão' (sem mesa)")
print("- Para criar pedido DELIVERY: Selecione cliente com endereço")
print("- Use /pedidos/rapido/ para pedidos rápidos sem cadastro")
print("- Senha de cancelamento: 1234")