from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from apps.pedidos.models import Pedido
from .models import Caixa, MovimentoCaixa

User = get_user_model()


@receiver(post_save, sender=Pedido)
def create_movimento_venda(sender, instance, created, **kwargs):
    """
    Cria movimento de caixa automaticamente quando um pedido é entregue
    """
    # Só processa se o pedido foi alterado para 'entregue'
    if not created and instance.status == 'entregue':
        # Verifica se já existe movimento para este pedido
        if MovimentoCaixa.objects.filter(
            categoria='vendas',
            descricao__contains=f'Pedido #{instance.id}'
        ).exists():
            return
        
        # Busca caixa aberto
        caixa_aberto = Caixa.objects.filter(status='aberto').first()
        if not caixa_aberto:
            return
        
        # Determina usuário para o movimento
        usuario = instance.usuario if instance.usuario else User.objects.filter(is_staff=True).first()
        if not usuario:
            return
        
        # Cria movimento de venda
        movimento = MovimentoCaixa.objects.create(
            caixa=caixa_aberto,
            usuario=usuario,
            tipo='entrada',
            categoria='vendas',
            descricao=f'Venda - Pedido #{instance.id}',
            valor=instance.total,
            observacoes=f'Pedido entregue para {instance.cliente.nome if instance.cliente else "Cliente"}\n'
                       f'Forma de pagamento: {instance.get_forma_pagamento_display()}\n'
                       f'Tipo: {instance.get_tipo_display()}'
        )
        
        print(f"DEBUG: Movimento de venda criado automaticamente - Pedido #{instance.id} - R$ {instance.total}")


@receiver(pre_save, sender=Pedido)
def track_pedido_status_change(sender, instance, **kwargs):
    """
    Rastreia mudanças de status do pedido para criar movimentos apropriados
    """
    if instance.pk:
        try:
            old_instance = Pedido.objects.get(pk=instance.pk)
            # Armazena o status anterior para comparação no post_save
            instance._old_status = old_instance.status
        except Pedido.DoesNotExist:
            instance._old_status = None
    else:
        instance._old_status = None


@receiver(post_save, sender=Pedido)
def handle_pedido_status_changes(sender, instance, created, **kwargs):
    """
    Lida com mudanças específicas de status do pedido
    """
    if created:
        return
    
    old_status = getattr(instance, '_old_status', None)
    
    # Se mudou de qualquer status para 'entregue', cria movimento de venda
    if old_status and old_status != 'entregue' and instance.status == 'entregue':
        create_movimento_venda(sender, instance, created, **kwargs)
    
    # Se mudou de 'entregue' para 'cancelado', remove/reverte movimento
    elif old_status == 'entregue' and instance.status == 'cancelado':
        reverse_movimento_venda(instance)


def reverse_movimento_venda(pedido):
    """
    Reverte movimento de venda quando pedido é cancelado após entrega
    """
    # Busca movimento relacionado ao pedido
    movimento = MovimentoCaixa.objects.filter(
        categoria='vendas',
        descricao__contains=f'Pedido #{pedido.id}',
        tipo='entrada'
    ).first()
    
    if not movimento:
        return
    
    # Busca caixa aberto
    caixa_aberto = Caixa.objects.filter(status='aberto').first()
    if not caixa_aberto:
        return
    
    # Determina usuário
    usuario = pedido.usuario if pedido.usuario else User.objects.filter(is_staff=True).first()
    if not usuario:
        return
    
    # Cria movimento de estorno
    MovimentoCaixa.objects.create(
        caixa=caixa_aberto,
        usuario=usuario,
        tipo='saida',
        categoria='estornos',
        descricao=f'Estorno - Pedido #{pedido.id} cancelado',
        valor=movimento.valor,
        observacoes=f'Estorno de venda cancelada\n'
                   f'Movimento original: {movimento.descricao}\n'
                   f'Data original: {movimento.data.strftime("%d/%m/%Y %H:%M")}'
    )
    
    print(f"DEBUG: Movimento de estorno criado - Pedido #{pedido.id} - R$ {movimento.valor}")


# Signal para criar movimentos de taxa de entrega separadamente (opcional)
@receiver(post_save, sender=Pedido)
def create_movimento_taxa_entrega(sender, instance, created, **kwargs):
    """
    Cria movimento separado para taxa de entrega se configurado
    """
    # Só processa se é delivery e tem taxa
    if (not created and 
        instance.status == 'entregue' and 
        instance.tipo == 'delivery' and 
        hasattr(instance, 'taxa_entrega') and 
        instance.taxa_entrega > 0):
        
        # Verifica se já existe movimento para esta taxa
        if MovimentoCaixa.objects.filter(
            categoria='taxa_entrega',
            descricao__contains=f'Pedido #{instance.id}'
        ).exists():
            return
        
        # Busca caixa aberto
        caixa_aberto = Caixa.objects.filter(status='aberto').first()
        if not caixa_aberto:
            return
        
        # Determina usuário
        usuario = instance.usuario if instance.usuario else User.objects.filter(is_staff=True).first()
        if not usuario:
            return
        
        # Cria movimento de taxa de entrega
        MovimentoCaixa.objects.create(
            caixa=caixa_aberto,
            usuario=usuario,
            tipo='entrada',
            categoria='taxa_entrega',
            descricao=f'Taxa de Entrega - Pedido #{instance.id}',
            valor=instance.taxa_entrega,
            observacoes=f'Taxa de entrega cobrada\n'
                       f'Endereço: {instance.endereco_entrega if hasattr(instance, "endereco_entrega") else "N/A"}'
        )
        
        print(f"DEBUG: Movimento de taxa de entrega criado - Pedido #{instance.id} - R$ {instance.taxa_entrega}")