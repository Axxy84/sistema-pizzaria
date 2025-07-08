from rest_framework import serializers
from .models import Caixa, MovimentoCaixa, ContaPagar
from django.utils import timezone

class CaixaListSerializer(serializers.ModelSerializer):
    usuario_nome = serializers.CharField(source='usuario.username', read_only=True)
    saldo_esperado = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    diferenca = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = Caixa
        fields = [
            'id', 'usuario_nome', 'status', 'valor_abertura', 'valor_fechamento',
            'saldo_esperado', 'diferenca', 'data_abertura', 'data_fechamento'
        ]

class MovimentoCaixaSerializer(serializers.ModelSerializer):
    usuario_nome = serializers.CharField(source='usuario.username', read_only=True)
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    categoria_display = serializers.CharField(source='get_categoria_display', read_only=True)
    pedido_numero = serializers.CharField(source='pedido.numero', read_only=True)
    
    class Meta:
        model = MovimentoCaixa
        fields = [
            'id', 'tipo', 'tipo_display', 'categoria', 'categoria_display',
            'descricao', 'valor', 'pedido', 'pedido_numero', 'usuario',
            'usuario_nome', 'data'
        ]
        read_only_fields = ['usuario', 'data']

class CaixaDetailSerializer(serializers.ModelSerializer):
    usuario = serializers.StringRelatedField()
    movimentos = MovimentoCaixaSerializer(many=True, read_only=True)
    saldo_esperado = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    diferenca = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    resumo = serializers.SerializerMethodField()
    
    class Meta:
        model = Caixa
        fields = [
            'id', 'usuario', 'status', 'valor_abertura', 'valor_fechamento',
            'saldo_esperado', 'diferenca', 'data_abertura', 'data_fechamento',
            'observacoes_abertura', 'observacoes_fechamento', 'movimentos', 'resumo'
        ]
        read_only_fields = ['data_abertura', 'data_fechamento']
    
    def get_resumo(self, obj):
        movimentos = obj.movimentos.all()
        return {
            'total_vendas': sum(m.valor for m in movimentos if m.categoria == 'venda'),
            'total_sangrias': sum(m.valor for m in movimentos if m.categoria == 'sangria'),
            'total_suprimentos': sum(m.valor for m in movimentos if m.categoria == 'suprimento'),
            'total_despesas': sum(m.valor for m in movimentos if m.categoria == 'despesa'),
            'total_movimentos': movimentos.count()
        }

class CaixaOpenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Caixa
        fields = ['valor_abertura', 'observacoes_abertura']

class CaixaCloseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Caixa
        fields = ['valor_fechamento', 'observacoes_fechamento']
    
    def update(self, instance, validated_data):
        instance.valor_fechamento = validated_data.get('valor_fechamento')
        instance.observacoes_fechamento = validated_data.get('observacoes_fechamento', '')
        instance.status = 'fechado'
        instance.data_fechamento = timezone.now()
        instance.save()
        return instance

class ContaPagarListSerializer(serializers.ModelSerializer):
    categoria_display = serializers.CharField(source='get_categoria_display', read_only=True)
    vencida = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = ContaPagar
        fields = [
            'id', 'descricao', 'categoria', 'categoria_display', 'valor',
            'data_vencimento', 'status', 'vencida'
        ]

class ContaPagarDetailSerializer(serializers.ModelSerializer):
    criado_por_nome = serializers.CharField(source='criado_por.username', read_only=True)
    pago_por_nome = serializers.CharField(source='pago_por.username', read_only=True)
    vencida = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = ContaPagar
        fields = [
            'id', 'descricao', 'categoria', 'valor', 'data_vencimento',
            'data_pagamento', 'status', 'vencida', 'observacoes',
            'criado_por', 'criado_por_nome', 'pago_por', 'pago_por_nome',
            'criado_em'
        ]
        read_only_fields = ['criado_por', 'pago_por', 'criado_em']

class ContaPagarPaySerializer(serializers.Serializer):
    data_pagamento = serializers.DateField()
    observacoes = serializers.CharField(required=False, allow_blank=True)