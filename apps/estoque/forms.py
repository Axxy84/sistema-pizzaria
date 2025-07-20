from django import forms
from .models import Ingrediente, MovimentoEstoque, UnidadeMedida

class IngredienteForm(forms.ModelForm):
    class Meta:
        model = Ingrediente
        fields = [
            'nome', 'unidade_medida', 'quantidade_estoque', 
            'estoque_minimo', 'custo_unitario', 'ativo'
        ]
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'block w-full rounded-md border-gray-300 shadow-sm focus:border-red-500 focus:ring-red-500',
                'placeholder': 'Nome do ingrediente'
            }),
            'unidade_medida': forms.Select(attrs={
                'class': 'block w-full rounded-md border-gray-300 shadow-sm focus:border-red-500 focus:ring-red-500'
            }),
            'quantidade_estoque': forms.NumberInput(attrs={
                'class': 'block w-full rounded-md border-gray-300 shadow-sm focus:border-red-500 focus:ring-red-500',
                'step': '0.001',
                'min': '0'
            }),
            'estoque_minimo': forms.NumberInput(attrs={
                'class': 'block w-full rounded-md border-gray-300 shadow-sm focus:border-red-500 focus:ring-red-500',
                'step': '0.001',
                'min': '0'
            }),
            'custo_unitario': forms.NumberInput(attrs={
                'class': 'block w-full rounded-md border-gray-300 shadow-sm focus:border-red-500 focus:ring-red-500',
                'step': '0.01',
                'min': '0'
            }),
            'ativo': forms.CheckboxInput(attrs={
                'class': 'h-4 w-4 text-red-600 focus:ring-red-500 border-gray-300 rounded'
            }),
        }
        labels = {
            'nome': 'Nome',
            'unidade_medida': 'Unidade de Medida',
            'quantidade_estoque': 'Quantidade em Estoque',
            'estoque_minimo': 'Estoque Mínimo',
            'custo_unitario': 'Custo Unitário (R$)',
            'ativo': 'Ativo',
        }

class MovimentoEstoqueForm(forms.ModelForm):
    class Meta:
        model = MovimentoEstoque
        fields = ['ingrediente', 'tipo', 'quantidade', 'custo_unitario', 'motivo']
        widgets = {
            'ingrediente': forms.Select(attrs={
                'class': 'block w-full rounded-md border-gray-300 shadow-sm focus:border-red-500 focus:ring-red-500',
                'required': True
            }),
            'tipo': forms.Select(attrs={
                'class': 'block w-full rounded-md border-gray-300 shadow-sm focus:border-red-500 focus:ring-red-500'
            }),
            'quantidade': forms.NumberInput(attrs={
                'class': 'block w-full rounded-md border-gray-300 shadow-sm focus:border-red-500 focus:ring-red-500',
                'step': '0.001',
                'min': '0.001',
                'required': True
            }),
            'custo_unitario': forms.NumberInput(attrs={
                'class': 'block w-full rounded-md border-gray-300 shadow-sm focus:border-red-500 focus:ring-red-500',
                'step': '0.01',
                'min': '0',
                'required': True
            }),
            'motivo': forms.TextInput(attrs={
                'class': 'block w-full rounded-md border-gray-300 shadow-sm focus:border-red-500 focus:ring-red-500',
                'placeholder': 'Motivo do movimento',
                'required': True
            }),
        }
        labels = {
            'ingrediente': 'Ingrediente',
            'tipo': 'Tipo de Movimento',
            'quantidade': 'Quantidade',
            'custo_unitario': 'Custo Unitário (R$)',
            'motivo': 'Motivo',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar apenas ingredientes ativos
        self.fields['ingrediente'].queryset = Ingrediente.objects.filter(ativo=True).order_by('nome')
        
        # Adicionar help text baseado no tipo
        self.fields['quantidade'].help_text = 'Para saídas e perdas, verifique se há estoque suficiente'
        self.fields['custo_unitario'].help_text = 'Custo unitário do produto no momento do movimento'

class UnidadeMedidaForm(forms.ModelForm):
    class Meta:
        model = UnidadeMedida
        fields = ['nome', 'sigla']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'block w-full rounded-md border-gray-300 shadow-sm focus:border-red-500 focus:ring-red-500',
                'placeholder': 'Ex: Quilograma'
            }),
            'sigla': forms.TextInput(attrs={
                'class': 'block w-full rounded-md border-gray-300 shadow-sm focus:border-red-500 focus:ring-red-500',
                'placeholder': 'Ex: kg',
                'maxlength': '10'
            }),
        }
        labels = {
            'nome': 'Nome da Unidade',
            'sigla': 'Sigla',
        }

class EstoqueFiltroForm(forms.Form):
    """Form para filtros da listagem de estoque"""
    ESTOQUE_CHOICES = [
        ('todos', 'Todos'),
        ('baixo', 'Estoque Baixo'),
        ('zerado', 'Estoque Zerado'),
    ]
    
    STATUS_CHOICES = [
        ('todos', 'Todos'),
        ('ativo', 'Ativo'),
        ('inativo', 'Inativo'),
    ]
    
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'block w-full rounded-md border-gray-300 shadow-sm focus:border-red-500 focus:ring-red-500',
            'placeholder': 'Buscar ingrediente...'
        }),
        label='Buscar'
    )
    
    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'block w-full rounded-md border-gray-300 shadow-sm focus:border-red-500 focus:ring-red-500'
        }),
        label='Status'
    )
    
    estoque = forms.ChoiceField(
        choices=ESTOQUE_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'block w-full rounded-md border-gray-300 shadow-sm focus:border-red-500 focus:ring-red-500'
        }),
        label='Estoque'
    )

class RelatorioMovimentosForm(forms.Form):
    """Form para filtros do relatório de movimentos"""
    data_inicio = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'block w-full rounded-md border-gray-300 shadow-sm focus:border-red-500 focus:ring-red-500',
            'type': 'date'
        }),
        label='Data Início'
    )
    
    data_fim = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'block w-full rounded-md border-gray-300 shadow-sm focus:border-red-500 focus:ring-red-500',
            'type': 'date'
        }),
        label='Data Fim'
    )
    
    tipo = forms.ChoiceField(
        choices=[('todos', 'Todos')] + MovimentoEstoque.TIPO_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'block w-full rounded-md border-gray-300 shadow-sm focus:border-red-500 focus:ring-red-500'
        }),
        label='Tipo de Movimento'
    )