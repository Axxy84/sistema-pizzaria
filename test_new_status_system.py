#!/usr/bin/env python
import os
import sys
import django
from datetime import datetime
from django.utils import timezone

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoProject.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from apps.pedidos.models import Pedido

print("=== Testando Sistema de Status Automático ===\n")

# Buscar um pedido de teste
pedido = Pedido.objects.first()

if not pedido:
    print("Nenhum pedido encontrado no banco de dados.")
    exit(1)

print(f"Pedido selecionado: #{pedido.numero}")
print(f"Status atual: {pedido.status} ({pedido.status_display})")
print(f"Criado em: {pedido.criado_em}")
print("\n--- Timestamps atuais ---")
print(f"Preparação iniciada em: {pedido.preparacao_iniciada_em}")
print(f"Saída confirmada em: {pedido.saida_confirmada_em}")
print(f"Entregue em: {pedido.entregue_em}")
print(f"Cancelado em: {pedido.cancelado_em}")

# Testar progressão de status
print("\n=== Testando Progressão de Status ===")

# 1. Iniciar preparo
if pedido.pode_iniciar_preparo:
    print("\n1. Iniciando preparo...")
    pedido.preparacao_iniciada_em = timezone.now()
    pedido.save()
    print(f"   Status após iniciar preparo: {pedido.status} ({pedido.status_display})")
else:
    print("\n1. Não é possível iniciar preparo (já iniciado ou cancelado)")

# 2. Confirmar saída (apenas delivery)
if pedido.pode_confirmar_saida:
    print("\n2. Confirmando saída para entrega...")
    pedido.saida_confirmada_em = timezone.now()
    pedido.save()
    print(f"   Status após confirmar saída: {pedido.status} ({pedido.status_display})")
else:
    print("\n2. Não é possível confirmar saída (não é delivery ou não está preparando)")

# 3. Confirmar entrega
if pedido.pode_confirmar_entrega:
    print("\n3. Confirmando entrega...")
    pedido.entregue_em = timezone.now()
    pedido.save()
    print(f"   Status após confirmar entrega: {pedido.status} ({pedido.status_display})")
else:
    print("\n3. Não é possível confirmar entrega (já entregue ou cancelado)")

# Testar cancelamento
print("\n=== Testando Cancelamento ===")
# Resetar pedido para testar cancelamento
pedido.preparacao_iniciada_em = None
pedido.saida_confirmada_em = None
pedido.entregue_em = None
pedido.cancelado_em = None
pedido.save()

print(f"Pedido resetado. Status: {pedido.status}")
print(f"Pode cancelar? {pedido.pode_cancelar}")

if pedido.pode_cancelar:
    print("Cancelando pedido...")
    pedido.cancelado_em = timezone.now()
    pedido.motivo_cancelamento = "Teste de cancelamento"
    pedido.save()
    print(f"Status após cancelar: {pedido.status} ({pedido.status_display})")
    print(f"Motivo: {pedido.motivo_cancelamento}")

print("\n=== Teste Concluído ===")