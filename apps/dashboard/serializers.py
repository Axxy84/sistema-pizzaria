from rest_framework import serializers
from datetime import datetime, timedelta
from django.db.models import Sum, Count, Avg
from apps.pedidos.models import Pedido
from apps.financeiro.models import MovimentoCaixa
from apps.estoque.models import Ingrediente
from apps.produtos.models import Produto

class DashboardSerializer(serializers.Serializer):
    """Serializer para dados do dashboard principal"""
    
    vendas_hoje = serializers.SerializerMethodField()
    vendas_mes = serializers.SerializerMethodField()
    pedidos_hoje = serializers.SerializerMethodField()
    ticket_medio = serializers.SerializerMethodField()
    produtos_em_falta = serializers.SerializerMethodField()
    pedidos_por_status = serializers.SerializerMethodField()
    formas_pagamento = serializers.SerializerMethodField()
    
    def get_vendas_hoje(self, obj):
        hoje = datetime.now().date()
        total = MovimentoCaixa.objects.filter(
            categoria='venda',
            data__date=hoje
        ).aggregate(total=Sum('valor'))['total'] or 0
        return total
    
    def get_vendas_mes(self, obj):
        inicio_mes = datetime.now().replace(day=1).date()
        total = MovimentoCaixa.objects.filter(
            categoria='venda',
            data__date__gte=inicio_mes
        ).aggregate(total=Sum('valor'))['total'] or 0
        return total
    
    def get_pedidos_hoje(self, obj):
        hoje = datetime.now().date()
        return Pedido.objects.filter(criado_em__date=hoje).count()
    
    def get_ticket_medio(self, obj):
        hoje = datetime.now().date()
        media = Pedido.objects.filter(
            criado_em__date=hoje,
            status='entregue'
        ).aggregate(media=Avg('total'))['media'] or 0
        return round(media, 2)
    
    def get_produtos_em_falta(self, obj):
        return Ingrediente.objects.filter(
            quantidade_estoque__lte=models.F('estoque_minimo'),
            ativo=True
        ).count()
    
    def get_pedidos_por_status(self, obj):
        hoje = datetime.now().date()
        status_count = Pedido.objects.filter(
            criado_em__date=hoje
        ).values('status').annotate(total=Count('id'))
        
        return {item['status']: item['total'] for item in status_count}
    
    def get_formas_pagamento(self, obj):
        hoje = datetime.now().date()
        pagamentos = Pedido.objects.filter(
            criado_em__date=hoje,
            status='entregue'
        ).values('forma_pagamento').annotate(
            total=Count('id'),
            valor=Sum('total')
        )
        
        return [
            {
                'forma': item['forma_pagamento'],
                'quantidade': item['total'],
                'valor': item['valor']
            }
            for item in pagamentos
        ]

class VendasPeriodoSerializer(serializers.Serializer):
    """Serializer para relatório de vendas por período"""
    
    data_inicio = serializers.DateField()
    data_fim = serializers.DateField()
    total_vendas = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_pedidos = serializers.IntegerField()
    ticket_medio = serializers.DecimalField(max_digits=10, decimal_places=2)
    vendas_por_dia = serializers.ListField()
    produtos_mais_vendidos = serializers.ListField()

class ProdutoRankingSerializer(serializers.Serializer):
    """Serializer para ranking de produtos"""
    
    produto_id = serializers.IntegerField()
    produto_nome = serializers.CharField()
    categoria = serializers.CharField()
    quantidade_vendida = serializers.IntegerField()
    valor_total = serializers.DecimalField(max_digits=10, decimal_places=2)