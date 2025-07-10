from django import forms
from django.core.exceptions import ValidationError
from decimal import Decimal
from .models import Produto, Categoria, Tamanho


class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = [
            'nome', 'descricao', 'categoria', 'tipo_produto',
            'preco_unitario', 'ingredientes', 'estoque_disponivel',
            'imagem', 'ativo'
        ]
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-red-500 focus:ring-red-500',
                'placeholder': 'Nome do produto'
            }),
            'descricao': forms.Textarea(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-red-500 focus:ring-red-500',
                'rows': 3,
                'placeholder': 'Descrição do produto'
            }),
            'categoria': forms.Select(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-red-500 focus:ring-red-500'
            }),
            'tipo_produto': forms.Select(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-red-500 focus:ring-red-500'
            }),
            'preco_unitario': forms.NumberInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-red-500 focus:ring-red-500',
                'placeholder': '0.00',
                'step': '0.01'
            }),
            'ingredientes': forms.Textarea(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-red-500 focus:ring-red-500',
                'rows': 2,
                'placeholder': 'Ex: Molho de tomate, mussarela, orégano'
            }),
            'estoque_disponivel': forms.NumberInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-red-500 focus:ring-red-500',
                'placeholder': '0'
            }),
            'imagem': forms.FileInput(attrs={
                'class': 'mt-1 block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-red-50 file:text-red-700 hover:file:bg-red-100'
            }),
            'ativo': forms.CheckboxInput(attrs={
                'class': 'rounded border-gray-300 text-red-600 shadow-sm focus:border-red-500 focus:ring-red-500'
            })
        }
        labels = {
            'nome': 'Nome do Produto',
            'descricao': 'Descrição',
            'categoria': 'Categoria',
            'tipo_produto': 'Tipo de Produto',
            'preco_unitario': 'Preço Unitário (R$)',
            'ingredientes': 'Ingredientes',
            'estoque_disponivel': 'Estoque Disponível',
            'imagem': 'Imagem do Produto',
            'ativo': 'Produto Ativo'
        }
        help_texts = {
            'preco_unitario': 'Deixe em branco para produtos com preços por tamanho',
            'ingredientes': 'Separe os ingredientes por vírgula',
            'estoque_disponivel': 'Use 0 para produtos sem controle de estoque'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Adicionar categoria vazia no início
        self.fields['categoria'].empty_label = "Selecione uma categoria"
        # Ordenar categorias ativas
        self.fields['categoria'].queryset = Categoria.objects.filter(ativo=True).order_by('nome')


class PizzaForm(forms.ModelForm):
    """Formulário específico para pizzas com campos de preço por tamanho"""
    
    class Meta:
        model = Produto
        fields = ['nome', 'descricao', 'categoria', 'ingredientes', 'imagem', 'ativo']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-red-500 focus:ring-red-500',
                'placeholder': 'Ex: Margherita'
            }),
            'descricao': forms.Textarea(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-red-500 focus:ring-red-500',
                'rows': 2,
                'placeholder': 'Descrição breve da pizza'
            }),
            'categoria': forms.Select(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-red-500 focus:ring-red-500'
            }),
            'ingredientes': forms.Textarea(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-red-500 focus:ring-red-500',
                'rows': 2,
                'placeholder': 'Ex: Molho de tomate, mussarela, manjericão, azeite'
            }),
            'imagem': forms.FileInput(attrs={
                'class': 'mt-1 block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-red-50 file:text-red-700 hover:file:bg-red-100'
            }),
            'ativo': forms.CheckboxInput(attrs={
                'class': 'rounded border-gray-300 text-red-600 shadow-sm focus:border-red-500 focus:ring-red-500'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Filtrar apenas categorias de pizza
        self.fields['categoria'].queryset = Categoria.objects.filter(
            ativo=True,
            nome__in=['Pizzas Tradicionais', 'Pizzas Especiais']
        ).order_by('nome')
        
        # Adicionar campos de preço dinamicamente para cada tamanho
        tamanhos = Tamanho.objects.filter(ativo=True).order_by('ordem')
        for tamanho in tamanhos:
            field_name = f'preco_{tamanho.nome.lower()}'
            self.fields[field_name] = forms.DecimalField(
                label=f'Preço {tamanho.nome}',
                required=True,
                max_digits=10,
                decimal_places=2,
                widget=forms.NumberInput(attrs={
                    'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-red-500 focus:ring-red-500',
                    'placeholder': '0.00',
                    'step': '0.01',
                    'min': '0.01'
                })
            )
    
    def clean(self):
        cleaned_data = super().clean()
        
        # Validar ordem crescente de preços
        tamanhos = Tamanho.objects.filter(ativo=True).order_by('ordem')
        precos = []
        
        for tamanho in tamanhos:
            field_name = f'preco_{tamanho.nome.lower()}'
            preco = cleaned_data.get(field_name)
            if preco:
                precos.append((tamanho.nome, preco))
        
        # Verificar se os preços estão em ordem crescente
        for i in range(1, len(precos)):
            if precos[i][1] <= precos[i-1][1]:
                raise ValidationError(
                    f'O preço de {precos[i][0]} (R$ {precos[i][1]}) deve ser maior que o preço de {precos[i-1][0]} (R$ {precos[i-1][1]})'
                )
        
        return cleaned_data