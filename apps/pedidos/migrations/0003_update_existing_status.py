# Generated migration to update existing status values

from django.db import migrations


def update_status_values(apps, schema_editor):
    """Atualizar valores de status existentes para os novos valores"""
    Pedido = apps.get_model('pedidos', 'Pedido')
    
    # Mapeamento de status antigos para novos
    status_mapping = {
        'pendente': 'recebido',
        'confirmado': 'recebido',
        'saiu_entrega': 'saindo',
        # 'preparando': 'preparando',  # Já está correto
        # 'entregue': 'entregue',     # Já está correto
        # 'cancelado': 'cancelado',   # Já está correto
    }
    
    for old_status, new_status in status_mapping.items():
        Pedido.objects.filter(status=old_status).update(status=new_status)


def reverse_status_values(apps, schema_editor):
    """Reverter valores de status para os antigos (caso necesssário)"""
    Pedido = apps.get_model('pedidos', 'Pedido')
    
    # Mapeamento reverso
    status_mapping = {
        'recebido': 'pendente',
        'saindo': 'saiu_entrega',
    }
    
    for new_status, old_status in status_mapping.items():
        Pedido.objects.filter(status=new_status).update(status=old_status)


class Migration(migrations.Migration):

    dependencies = [
        ('pedidos', '0002_alter_pedido_status'),
    ]

    operations = [
        migrations.RunPython(update_status_values, reverse_status_values),
    ]