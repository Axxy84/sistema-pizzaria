from apps.pedidos.models import Pedido
from django.utils import timezone

def global_context(request):
    """
    Context processor para adicionar dados globais em todos os templates
    """
    context = {}
    
    if request.user.is_authenticated:
        # Pedidos pendentes para badge
        context['pedidos_pendentes'] = Pedido.objects.filter(
            cancelado_em__isnull=True,
            entregue_em__isnull=True
        ).count()
        
        # Verificar estoque baixo (exemplo simples)
        context['estoque_baixo'] = 0
        
        # Notificações
        context['notificacoes'] = context['pedidos_pendentes']
    
    # Layout preference
    context['use_clean_layout'] = getattr(request, 'use_clean_layout', True)
    
    return context