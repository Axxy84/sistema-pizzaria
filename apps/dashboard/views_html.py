from django.shortcuts import render
from django.db.models import Count, Sum, Q
from datetime import datetime, timedelta
from apps.pedidos.models import Pedido
from apps.produtos.models import Produto
from apps.clientes.models import Cliente

def dashboard_view(request):
    """View HTML do dashboard principal"""
    hoje = datetime.now().date()
    inicio_mes = hoje.replace(day=1)
    
    context = {
        # Estatísticas de hoje
        'pedidos_hoje': Pedido.objects.filter(criado_em__date=hoje).count(),
        'vendas_hoje': Pedido.objects.filter(
            criado_em__date=hoje, 
            status__in=['entregue', 'saindo']
        ).aggregate(total=Sum('total'))['total'] or 0,
        
        # Estatísticas do mês
        'pedidos_mes': Pedido.objects.filter(criado_em__date__gte=inicio_mes).count(),
        'vendas_mes': Pedido.objects.filter(
            criado_em__date__gte=inicio_mes,
            status__in=['entregue', 'saindo']
        ).aggregate(total=Sum('total'))['total'] or 0,
        
        # Pedidos por status
        'pedidos_pendentes': Pedido.objects.filter(status='recebido').count(),
        'pedidos_preparando': Pedido.objects.filter(status='preparando').count(),
        'pedidos_saindo': Pedido.objects.filter(status='saindo').count(),
        
        # Últimos pedidos
        'ultimos_pedidos': Pedido.objects.select_related('cliente').order_by('-criado_em')[:10],
        
        # Produtos mais vendidos
        'produtos_populares': Produto.objects.filter(ativo=True)[:5],
        
        # Total de clientes
        'total_clientes': Cliente.objects.filter(ativo=True).count(),
    }
    
    return render(request, 'dashboard/dashboard.html', context)
