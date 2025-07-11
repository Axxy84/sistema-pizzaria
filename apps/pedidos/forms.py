from django import forms
from django.forms import inlineformset_factory
from .models import Pedido, ItemPedido
from apps.clientes.models import Cliente, Endereco


class PedidoForm(forms.ModelForm):
    """Formulário principal do pedido"""
    
    class Meta:
        model = Pedido
        fields = [
            'cliente', 'tipo', 'endereco_entrega', 'mesa',
            'forma_pagamento', 'precisa_troco', 'troco_para',
            'taxa_entrega', 'desconto', 'observacoes'
        ]
        widgets = {
            'cliente': forms.Select(attrs={
                'class': 'form-select',
                'x-model': 'clienteId',
                '@change': 'buscarEnderecos()'
            }),
            'tipo': forms.RadioSelect(attrs={
                'class': 'form-radio',
                'x-model': 'tipoPedido'
            }),
            'endereco_entrega': forms.Select(attrs={
                'class': 'form-select',
                'x-show': "tipoPedido === 'delivery'"
            }),
            'mesa': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Número da mesa',
                'x-show': "tipoPedido === 'mesa'"
            }),
            'forma_pagamento': forms.Select(attrs={
                'class': 'form-select',
                'x-model': 'formaPagamento'
            }),
            'precisa_troco': forms.CheckboxInput(attrs={
                'class': 'form-checkbox',
                'x-model': 'precisaTroco',
                'x-show': "formaPagamento === 'dinheiro'"
            }),
            'troco_para': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': '0,00',
                'x-show': "precisaTroco && formaPagamento === 'dinheiro'",
                'step': '0.01'
            }),
            'taxa_entrega': forms.NumberInput(attrs={
                'class': 'form-input',
                'readonly': True,
                'x-model': 'taxaEntrega',
                'step': '0.01'
            }),
            'desconto': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': '0,00',
                'x-model': 'desconto',
                '@input': 'calcularTotal()',
                'step': '0.01'
            }),
            'observacoes': forms.Textarea(attrs={
                'class': 'form-textarea',
                'rows': 3,
                'placeholder': 'Observações do pedido...'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Tornar campos condicionais não obrigatórios
        self.fields['endereco_entrega'].required = False
        self.fields['mesa'].required = False
        self.fields['troco_para'].required = False
        
        # Personalizar labels
        self.fields['precisa_troco'].label = 'Precisa de troco?'
        self.fields['troco_para'].label = 'Troco para'
        self.fields['taxa_entrega'].label = 'Taxa de entrega'
    
    def clean(self):
        cleaned_data = super().clean()
        tipo = cleaned_data.get('tipo')
        endereco_entrega = cleaned_data.get('endereco_entrega')
        mesa = cleaned_data.get('mesa')
        forma_pagamento = cleaned_data.get('forma_pagamento')
        precisa_troco = cleaned_data.get('precisa_troco')
        troco_para = cleaned_data.get('troco_para')
        
        # Validações condicionais
        if tipo == 'delivery' and not endereco_entrega:
            self.add_error('endereco_entrega', 'Endereço de entrega é obrigatório para delivery')
        
        if tipo == 'mesa' and not mesa:
            self.add_error('mesa', 'Número da mesa é obrigatório')
        
        if forma_pagamento == 'dinheiro' and precisa_troco and not troco_para:
            self.add_error('troco_para', 'Informe o valor para troco')
        
        return cleaned_data


class ItemPedidoForm(forms.ModelForm):
    """Formulário para itens do pedido"""
    
    class Meta:
        model = ItemPedido
        fields = ['produto_preco', 'quantidade', 'observacoes']
        widgets = {
            'produto_preco': forms.Select(attrs={
                'class': 'form-select item-produto',
                '@change': 'atualizarPrecoItem($event)'
            }),
            'quantidade': forms.NumberInput(attrs={
                'class': 'form-input item-quantidade',
                'min': '1',
                '@input': 'atualizarSubtotalItem($event)'
            }),
            'observacoes': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Ex: Sem cebola, bem passada...'
            })
        }


# FormSet para múltiplos itens
ItemPedidoFormSet = inlineformset_factory(
    Pedido,
    ItemPedido,
    form=ItemPedidoForm,
    extra=1,
    can_delete=True,
    min_num=1,
    validate_min=True,
    fields=['produto_preco', 'quantidade', 'observacoes']
)


class ClienteRapidoForm(forms.ModelForm):
    """Formulário para cadastro rápido de cliente"""
    
    class Meta:
        model = Cliente
        fields = ['nome', 'telefone', 'email']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Nome completo',
                'required': True
            }),
            'telefone': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': '(00) 00000-0000',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-input',
                'placeholder': 'email@exemplo.com'
            })
        }


class EnderecoRapidoForm(forms.ModelForm):
    """Formulário para cadastro rápido de endereço"""
    
    class Meta:
        model = Endereco
        fields = [
            'cep', 'logradouro', 'numero', 'complemento',
            'bairro', 'cidade', 'estado', 'referencia'
        ]
        widgets = {
            'cep': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': '00000-000',
                'x-mask': '99999-999',
                '@blur': 'buscarCep($event)'
            }),
            'logradouro': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Rua, Avenida...'
            }),
            'numero': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Número'
            }),
            'complemento': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Apto, Bloco...'
            }),
            'bairro': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Bairro'
            }),
            'cidade': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Cidade'
            }),
            'estado': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'UF',
                'maxlength': '2'
            }),
            'referencia': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Ponto de referência'
            })
        }


class StatusUpdateForm(forms.ModelForm):
    """Formulário para atualizar status do pedido"""
    
    class Meta:
        model = Pedido
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={
                'class': 'form-select'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Definir transições válidas baseado no status atual
        if self.instance.pk:
            status_atual = self.instance.status
            transicoes_validas = {
                'pendente': ['confirmado', 'cancelado'],
                'confirmado': ['preparando', 'cancelado'],
                'preparando': ['saiu_entrega', 'cancelado'],
                'saiu_entrega': ['entregue', 'cancelado'],
                'entregue': [],
                'cancelado': []
            }
            
            opcoes_validas = transicoes_validas.get(status_atual, [])
            if opcoes_validas:
                self.fields['status'].choices = [
                    (k, v) for k, v in Pedido.STATUS_CHOICES 
                    if k in opcoes_validas
                ]
            else:
                self.fields['status'].widget.attrs['disabled'] = True