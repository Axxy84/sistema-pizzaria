from rest_framework import serializers
from .models import Pedido, ItemPedido
from apps.clientes.models import Cliente
from apps.clientes.serializers import ClienteListSerializer, EnderecoSerializer
from apps.produtos.serializers import ProdutoPrecoSerializer

class ItemPedidoSerializer(serializers.ModelSerializer):
    produto_nome = serializers.CharField(source='produto_preco.produto.nome', read_only=True)
    tamanho_nome = serializers.CharField(source='produto_preco.tamanho.nome', read_only=True)
    
    class Meta:
        model = ItemPedido
        fields = [
            'id', 'produto_preco', 'produto_nome', 'tamanho_nome',
            'quantidade', 'preco_unitario', 'subtotal', 'observacoes'
        ]
        read_only_fields = ['preco_unitario', 'subtotal']

class PedidoListSerializer(serializers.ModelSerializer):
    cliente_nome = serializers.CharField(source='cliente.nome', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    
    class Meta:
        model = Pedido
        fields = [
            'id', 'numero', 'cliente_nome', 'tipo', 'tipo_display',
            'status', 'status_display', 'total', 'criado_em'
        ]

class PedidoDetailSerializer(serializers.ModelSerializer):
    cliente = ClienteListSerializer(read_only=True)
    cliente_id = serializers.PrimaryKeyRelatedField(
        queryset=Cliente.objects.all(),
        source='cliente',
        write_only=True
    )
    endereco_entrega = EnderecoSerializer(read_only=True)
    itens = ItemPedidoSerializer(many=True, read_only=True)
    usuario_nome = serializers.CharField(source='usuario.username', read_only=True)
    
    class Meta:
        model = Pedido
        fields = [
            'id', 'numero', 'cliente', 'cliente_id', 'usuario', 'usuario_nome',
            'tipo', 'endereco_entrega', 'mesa', 'status', 'forma_pagamento',
            'precisa_troco', 'troco_para', 'subtotal', 'taxa_entrega',
            'desconto', 'total', 'observacoes', 'itens', 'criado_em', 'atualizado_em'
        ]
        read_only_fields = ['numero', 'usuario', 'subtotal', 'total', 'criado_em', 'atualizado_em']

class PedidoCreateSerializer(serializers.ModelSerializer):
    itens = ItemPedidoSerializer(many=True)
    
    class Meta:
        model = Pedido
        fields = [
            'cliente', 'tipo', 'endereco_entrega', 'mesa', 'forma_pagamento',
            'precisa_troco', 'troco_para', 'taxa_entrega', 'desconto',
            'observacoes', 'itens'
        ]
    
    def create(self, validated_data):
        itens_data = validated_data.pop('itens')
        pedido = Pedido.objects.create(**validated_data)
        
        for item_data in itens_data:
            ItemPedido.objects.create(pedido=pedido, **item_data)
        
        pedido.calcular_total()
        return pedido

class PedidoStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = ['status']
    
    def validate_status(self, value):
        pedido = self.instance
        status_atual = pedido.status
        
        # Validar transições de status
        transicoes_validas = {
            'pendente': ['confirmado', 'cancelado'],
            'confirmado': ['preparando', 'cancelado'],
            'preparando': ['saiu_entrega', 'cancelado'],
            'saiu_entrega': ['entregue', 'cancelado'],
            'entregue': [],
            'cancelado': []
        }
        
        if value not in transicoes_validas.get(status_atual, []):
            raise serializers.ValidationError(
                f"Não é possível mudar de '{status_atual}' para '{value}'"
            )
        
        return value