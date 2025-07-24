from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime, timedelta
from django.db.models import Sum, Count, Avg, F
from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from apps.core.cache_utils import cache_result, get_cached_or_compute, CacheManager
from apps.pedidos.models import Pedido, ItemPedido
from apps.produtos.models import Produto
from apps.estoque.models import Ingrediente
from apps.financeiro.models import MovimentoCaixa
from .serializers import (
    DashboardSerializer, VendasPeriodoSerializer,
    ProdutoRankingSerializer
)

class DashboardView(APIView):
    def get(self, request):
        # Tenta pegar dados do cache
        cache_key = 'dashboard:stats:main'
        data = cache.get(cache_key)
        
        if data is None:
            # Se não estiver no cache, calcula os dados
            serializer = DashboardSerializer(data={})
            data = {
                'vendas_hoje': serializer.get_vendas_hoje(None),
                'vendas_mes': serializer.get_vendas_mes(None),
                'pedidos_hoje': serializer.get_pedidos_hoje(None),
                'ticket_medio': serializer.get_ticket_medio(None),
                'produtos_em_falta': serializer.get_produtos_em_falta(None),
                'pedidos_por_status': serializer.get_pedidos_por_status(None),
                'formas_pagamento': serializer.get_formas_pagamento(None),
            }
            # Cache por 5 minutos
            cache.set(cache_key, data, 300)
        
        return Response(data)

class VendasPeriodoView(APIView):
    def get(self, request):
        # Pega parâmetros da query
        data_inicio = request.query_params.get('data_inicio')
        data_fim = request.query_params.get('data_fim')
        
        if not data_inicio or not data_fim:
            # Padrão: últimos 30 dias
            data_fim = datetime.now().date()
            data_inicio = data_fim - timedelta(days=30)
        else:
            data_inicio = datetime.strptime(data_inicio, '%Y-%m-%d').date()
            data_fim = datetime.strptime(data_fim, '%Y-%m-%d').date()
        
        # Cache key baseada no período
        cache_key = f"vendas:periodo:{data_inicio}:{data_fim}"
        
        # Calcula métricas
        pedidos = Pedido.objects.filter(
            criado_em__date__gte=data_inicio,
            criado_em__date__lte=data_fim,
            status='entregue'
        )
        
        total_vendas = pedidos.aggregate(total=Sum('total'))['total'] or 0
        total_pedidos = pedidos.count()
        ticket_medio = pedidos.aggregate(media=Avg('total'))['media'] or 0
        
        # Vendas por dia
        vendas_por_dia = []
        current_date = data_inicio
        while current_date <= data_fim:
            vendas_dia = pedidos.filter(
                criado_em__date=current_date
            ).aggregate(total=Sum('total'))['total'] or 0
            
            vendas_por_dia.append({
                'data': current_date.strftime('%Y-%m-%d'),
                'total': vendas_dia
            })
            current_date += timedelta(days=1)
        
        # Produtos mais vendidos
        produtos_vendidos = ItemPedido.objects.filter(
            pedido__in=pedidos
        ).values(
            'produto_preco__produto__id',
            'produto_preco__produto__nome',
            'produto_preco__produto__categoria__nome'
        ).annotate(
            quantidade_total=Sum('quantidade'),
            valor_total=Sum('subtotal')
        ).order_by('-quantidade_total')[:10]
        
        produtos_mais_vendidos = [
            {
                'produto_id': item['produto_preco__produto__id'],
                'produto_nome': item['produto_preco__produto__nome'],
                'categoria': item['produto_preco__produto__categoria__nome'],
                'quantidade_vendida': item['quantidade_total'],
                'valor_total': item['valor_total']
            }
            for item in produtos_vendidos
        ]
        
        data = {
            'data_inicio': data_inicio,
            'data_fim': data_fim,
            'total_vendas': total_vendas,
            'total_pedidos': total_pedidos,
            'ticket_medio': round(ticket_medio, 2),
            'vendas_por_dia': vendas_por_dia,
            'produtos_mais_vendidos': produtos_mais_vendidos
        }
        
        return Response(data)

class ProdutosRankingView(APIView):
    def get(self, request):
        # Pega parâmetros
        periodo = request.query_params.get('periodo', 'mes')  # dia, semana, mes
        limite = int(request.query_params.get('limite', 10))
        
        # Define data inicial baseada no período
        data_fim = datetime.now().date()
        if periodo == 'dia':
            data_inicio = data_fim
        elif periodo == 'semana':
            data_inicio = data_fim - timedelta(days=7)
        else:  # mes
            data_inicio = data_fim - timedelta(days=30)
        
        # Query para ranking
        ranking = ItemPedido.objects.filter(
            pedido__criado_em__date__gte=data_inicio,
            pedido__criado_em__date__lte=data_fim,
            pedido__status='entregue'
        ).values(
            'produto_preco__produto__id',
            'produto_preco__produto__nome',
            'produto_preco__produto__categoria__nome'
        ).annotate(
            quantidade_vendida=Sum('quantidade'),
            valor_total=Sum('subtotal')
        ).order_by('-quantidade_vendida')[:limite]
        
        data = [
            {
                'produto_id': item['produto_preco__produto__id'],
                'produto_nome': item['produto_preco__produto__nome'],
                'categoria': item['produto_preco__produto__categoria__nome'],
                'quantidade_vendida': item['quantidade_vendida'],
                'valor_total': item['valor_total']
            }
            for item in ranking
        ]
        
        return Response(data)