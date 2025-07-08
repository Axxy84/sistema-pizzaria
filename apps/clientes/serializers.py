from rest_framework import serializers
from .models import Cliente, Endereco

class EnderecoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Endereco
        fields = [
            'id', 'tipo', 'cep', 'logradouro', 'numero', 'complemento',
            'bairro', 'cidade', 'estado', 'referencia', 'principal'
        ]

class ClienteListSerializer(serializers.ModelSerializer):
    total_pedidos = serializers.IntegerField(source='pedidos.count', read_only=True)
    
    class Meta:
        model = Cliente
        fields = ['id', 'nome', 'telefone', 'email', 'ativo', 'total_pedidos']

class ClienteDetailSerializer(serializers.ModelSerializer):
    enderecos = EnderecoSerializer(many=True, read_only=True)
    total_pedidos = serializers.IntegerField(source='pedidos.count', read_only=True)
    
    class Meta:
        model = Cliente
        fields = [
            'id', 'nome', 'email', 'telefone', 'telefone2', 'cpf',
            'data_nascimento', 'observacoes', 'ativo', 'enderecos',
            'total_pedidos', 'criado_em', 'atualizado_em'
        ]
        read_only_fields = ['criado_em', 'atualizado_em']
    
    def validate_cpf(self, value):
        if value:
            # Remove caracteres não numéricos
            cpf = ''.join(filter(str.isdigit, value))
            if len(cpf) != 11:
                raise serializers.ValidationError("CPF deve ter 11 dígitos")
            return cpf
        return value

class ClienteCreateSerializer(serializers.ModelSerializer):
    endereco = EnderecoSerializer(write_only=True, required=False)
    
    class Meta:
        model = Cliente
        fields = [
            'nome', 'email', 'telefone', 'telefone2', 'cpf',
            'data_nascimento', 'observacoes', 'endereco'
        ]
    
    def create(self, validated_data):
        endereco_data = validated_data.pop('endereco', None)
        cliente = Cliente.objects.create(**validated_data)
        
        if endereco_data:
            endereco_data['principal'] = True
            Endereco.objects.create(cliente=cliente, **endereco_data)
        
        return cliente