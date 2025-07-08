from rest_framework import serializers
from .models import UnidadeMedida, Ingrediente, MovimentoEstoque, ReceitaProduto

class UnidadeMedidaSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnidadeMedida
        fields = ['id', 'nome', 'sigla']

class IngredienteListSerializer(serializers.ModelSerializer):
    unidade_medida_sigla = serializers.CharField(source='unidade_medida.sigla', read_only=True)
    estoque_baixo = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Ingrediente
        fields = [
            'id', 'nome', 'unidade_medida_sigla', 'quantidade_estoque',
            'estoque_minimo', 'estoque_baixo', 'custo_unitario', 'ativo'
        ]

class IngredienteDetailSerializer(serializers.ModelSerializer):
    unidade_medida = UnidadeMedidaSerializer(read_only=True)
    unidade_medida_id = serializers.PrimaryKeyRelatedField(
        queryset=UnidadeMedida.objects.all(),
        source='unidade_medida',
        write_only=True
    )
    estoque_baixo = serializers.BooleanField(read_only=True)
    valor_estoque = serializers.SerializerMethodField()
    
    class Meta:
        model = Ingrediente
        fields = [
            'id', 'nome', 'unidade_medida', 'unidade_medida_id',
            'quantidade_estoque', 'estoque_minimo', 'estoque_baixo',
            'custo_unitario', 'valor_estoque', 'ativo', 'criado_em', 'atualizado_em'
        ]
        read_only_fields = ['criado_em', 'atualizado_em']
    
    def get_valor_estoque(self, obj):
        return obj.quantidade_estoque * obj.custo_unitario

class MovimentoEstoqueSerializer(serializers.ModelSerializer):
    ingrediente_nome = serializers.CharField(source='ingrediente.nome', read_only=True)
    usuario_nome = serializers.CharField(source='usuario.username', read_only=True)
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    
    class Meta:
        model = MovimentoEstoque
        fields = [
            'id', 'ingrediente', 'ingrediente_nome', 'tipo', 'tipo_display',
            'quantidade', 'custo_unitario', 'custo_total', 'motivo',
            'usuario', 'usuario_nome', 'data'
        ]
        read_only_fields = ['custo_total', 'usuario', 'data']

class MovimentoEstoqueCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovimentoEstoque
        fields = ['ingrediente', 'tipo', 'quantidade', 'custo_unitario', 'motivo']
    
    def validate(self, data):
        # Validar se há estoque suficiente para saída/perda
        if data['tipo'] in ['saida', 'perda']:
            ingrediente = data['ingrediente']
            if ingrediente.quantidade_estoque < data['quantidade']:
                raise serializers.ValidationError({
                    'quantidade': f'Estoque insuficiente. Disponível: {ingrediente.quantidade_estoque}'
                })
        return data

class ReceitaProdutoSerializer(serializers.ModelSerializer):
    ingrediente_nome = serializers.CharField(source='ingrediente.nome', read_only=True)
    unidade_medida = serializers.CharField(source='ingrediente.unidade_medida.sigla', read_only=True)
    custo = serializers.SerializerMethodField()
    
    class Meta:
        model = ReceitaProduto
        fields = [
            'id', 'produto', 'ingrediente', 'ingrediente_nome',
            'quantidade', 'unidade_medida', 'custo'
        ]
    
    def get_custo(self, obj):
        return obj.quantidade * obj.ingrediente.custo_unitario