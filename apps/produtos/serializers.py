from rest_framework import serializers
from .models import Categoria, Tamanho, Produto, ProdutoPreco

class CategoriaSerializer(serializers.ModelSerializer):
    produtos_count = serializers.IntegerField(source='produtos.count', read_only=True)
    
    class Meta:
        model = Categoria
        fields = ['id', 'nome', 'descricao', 'ativo', 'produtos_count', 'criado_em', 'atualizado_em']
        read_only_fields = ['criado_em', 'atualizado_em']

class TamanhoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tamanho
        fields = ['id', 'nome', 'ordem', 'ativo']

class ProdutoPrecoSerializer(serializers.ModelSerializer):
    tamanho_nome = serializers.CharField(source='tamanho.nome', read_only=True)
    preco_final = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = ProdutoPreco
        fields = ['id', 'tamanho', 'tamanho_nome', 'preco', 'preco_promocional', 'preco_final']

class ProdutoListSerializer(serializers.ModelSerializer):
    categoria_nome = serializers.CharField(source='categoria.nome', read_only=True)
    preco_minimo = serializers.SerializerMethodField()
    
    class Meta:
        model = Produto
        fields = ['id', 'nome', 'categoria', 'categoria_nome', 'imagem', 'ativo', 'preco_minimo']
    
    def get_preco_minimo(self, obj):
        precos = obj.precos.filter(tamanho__ativo=True)
        if precos:
            return min(p.preco_final for p in precos)
        return None

class ProdutoDetailSerializer(serializers.ModelSerializer):
    categoria = CategoriaSerializer(read_only=True)
    categoria_id = serializers.PrimaryKeyRelatedField(
        queryset=Categoria.objects.all(),
        source='categoria',
        write_only=True
    )
    precos = ProdutoPrecoSerializer(many=True, read_only=True)
    
    class Meta:
        model = Produto
        fields = [
            'id', 'nome', 'descricao', 'categoria', 'categoria_id', 
            'imagem', 'ativo', 'precos', 'criado_em', 'atualizado_em'
        ]
        read_only_fields = ['criado_em', 'atualizado_em']