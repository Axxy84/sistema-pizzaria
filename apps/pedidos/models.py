from django.db import models
from django.contrib.auth.models import User
from apps.clientes.models import Cliente, Endereco
from apps.produtos.models import Produto, ProdutoPreco
from decimal import Decimal
import json

class Pedido(models.Model):
    STATUS_CHOICES = [
        ('recebido', 'Recebido'),
        ('preparando', 'Preparando'),
        ('saindo', 'Saindo'),
        ('entregue', 'Entregue'),
        ('cancelado', 'Cancelado'),
    ]
    
    TIPO_CHOICES = [
        ('delivery', 'Delivery'),
        ('balcao', 'Balcão'),
        ('mesa', 'Mesa'),
    ]
    
    PAGAMENTO_CHOICES = [
        ('dinheiro', 'Dinheiro'),
        ('pix', 'PIX'),
        ('cartao_credito', 'Cartão de Crédito'),
        ('cartao_debito', 'Cartão de Débito'),
        ('vale_refeicao', 'Vale Refeição'),
    ]
    
    # Identificação
    numero = models.CharField(max_length=20, unique=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name='pedidos')
    usuario = models.ForeignKey(User, on_delete=models.PROTECT, related_name='pedidos_atendidos')
    
    # Tipo e endereço
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    endereco_entrega = models.ForeignKey(
        Endereco, 
        on_delete=models.PROTECT, 
        null=True, 
        blank=True,
        related_name='pedidos'
    )
    mesa = models.CharField(max_length=10, blank=True)
    
    # Status e pagamento
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='recebido')
    forma_pagamento = models.CharField(max_length=20, choices=PAGAMENTO_CHOICES)
    precisa_troco = models.BooleanField(default=False)
    troco_para = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Valores
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    taxa_entrega = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    desconto = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Observações
    observacoes = models.TextField(blank=True)
    
    # Datas
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'
        ordering = ['-criado_em']
    
    def __str__(self):
        # Avoid potential circular references by using getattr with defaults
        numero = getattr(self, 'numero', 'N/A')
        cliente_nome = getattr(self.cliente, 'nome', 'Cliente') if hasattr(self, 'cliente') and self.cliente else 'Sem Cliente'
        return f"Pedido #{numero} - {cliente_nome}"
    
    def calcular_total(self):
        # Use aggregate to avoid loading all objects into memory
        from django.db.models import Sum
        total_itens = self.itens.aggregate(total=Sum('subtotal'))['total'] or Decimal('0')
        self.subtotal = total_itens
        self.total = self.subtotal + self.taxa_entrega - self.desconto
        # Use update_fields to only update specific fields and avoid triggering signals
        self.save(update_fields=['subtotal', 'total', 'atualizado_em'])
    
    def save(self, *args, **kwargs):
        if not self.numero:
            # Gerar número do pedido
            ultimo = Pedido.objects.all().order_by('-id').first()
            if ultimo and ultimo.numero.isdigit():
                self.numero = str(int(ultimo.numero) + 1).zfill(6)
            else:
                # If no valid numeric number exists, start from 000001
                self.numero = '000001'
        super().save(*args, **kwargs)

class ItemPedido(models.Model):
    REGRA_PRECO_MEIO_A_MEIO = [
        ('mais_caro', 'Preço do sabor mais caro'),
        ('media', 'Média dos dois preços'),
        ('personalizado', 'Preço personalizado'),
    ]
    
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='itens')
    produto_preco = models.ForeignKey(ProdutoPreco, on_delete=models.PROTECT)
    quantidade = models.IntegerField(default=1)
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    observacoes = models.TextField(blank=True)
    
    # Campo para armazenar dados de pizza meio a meio
    meio_a_meio_data = models.JSONField(null=True, blank=True, help_text='Dados da personalização meio a meio')
    
    class Meta:
        verbose_name = 'Item do Pedido'
        verbose_name_plural = 'Itens do Pedido'
    
    def __str__(self):
        # Safer string representation to avoid circular references
        try:
            produto_nome = self.produto_preco.produto.nome if self.produto_preco and self.produto_preco.produto else 'Produto'
            return f"{self.quantidade}x {produto_nome}"
        except:
            return f"Item {self.id or 'Novo'}"
    
    @property
    def is_meio_a_meio(self):
        """Verifica se o item é uma pizza meio a meio"""
        return self.meio_a_meio_data is not None and self.meio_a_meio_data.get('is_meio_a_meio', False)
    
    @property
    def sabor_1(self):
        """Retorna dados do primeiro sabor se for meio a meio"""
        if self.is_meio_a_meio:
            return self.meio_a_meio_data.get('sabor_1')
        return None
    
    @property
    def sabor_2(self):
        """Retorna dados do segundo sabor se for meio a meio"""
        if self.is_meio_a_meio:
            return self.meio_a_meio_data.get('sabor_2')
        return None
    
    def configurar_meio_a_meio(self, produto_1, produto_2, tamanho, regra_preco='mais_caro'):
        """
        Configura o item como pizza meio a meio
        
        Args:
            produto_1: Produto do primeiro sabor
            produto_2: Produto do segundo sabor  
            tamanho: Objeto Tamanho
            regra_preco: 'mais_caro', 'media' ou 'personalizado'
        """
        # Buscar preços dos dois sabores no tamanho escolhido
        try:
            preco_1 = ProdutoPreco.objects.get(produto=produto_1, tamanho=tamanho)
            preco_2 = ProdutoPreco.objects.get(produto=produto_2, tamanho=tamanho)
        except ProdutoPreco.DoesNotExist:
            raise ValueError("Um dos sabores não possui preço para o tamanho selecionado")
        
        # Configurar dados do meio a meio
        self.meio_a_meio_data = {
            'is_meio_a_meio': True,
            'sabor_1': {
                'produto_id': produto_1.id,
                'nome': produto_1.nome,
                'preco': float(preco_1.preco_final)
            },
            'sabor_2': {
                'produto_id': produto_2.id,
                'nome': produto_2.nome,
                'preco': float(preco_2.preco_final)
            },
            'tamanho': tamanho.nome,
            'regra_preco': regra_preco
        }
        
        # Calcular preço baseado na regra
        if regra_preco == 'mais_caro':
            self.preco_unitario = max(preco_1.preco_final, preco_2.preco_final)
        elif regra_preco == 'media':
            self.preco_unitario = (preco_1.preco_final + preco_2.preco_final) / 2
        
        # Usar o produto_preco do sabor mais caro para referência
        self.produto_preco = preco_1 if preco_1.preco_final >= preco_2.preco_final else preco_2
    
    def calcular_preco_meio_a_meio(self):
        """Calcula o preço baseado na regra configurada"""
        if not self.is_meio_a_meio:
            return self.preco_unitario
        
        sabor_1_preco = Decimal(str(self.sabor_1.get('preco', 0)))
        sabor_2_preco = Decimal(str(self.sabor_2.get('preco', 0)))
        regra = self.meio_a_meio_data.get('regra_preco', 'mais_caro')
        
        if regra == 'mais_caro':
            return max(sabor_1_preco, sabor_2_preco)
        elif regra == 'media':
            return (sabor_1_preco + sabor_2_preco) / 2
        else:
            return self.preco_unitario
    
    def get_descricao_completa(self):
        """Retorna descrição completa do item, incluindo meio a meio"""
        if self.is_meio_a_meio:
            sabor_1_nome = self.sabor_1.get('nome', 'Sabor 1')
            sabor_2_nome = self.sabor_2.get('nome', 'Sabor 2')
            tamanho = self.meio_a_meio_data.get('tamanho', '')
            return f"Pizza {tamanho} - Meio a Meio: {sabor_1_nome} + {sabor_2_nome}"
        else:
            return f"{self.produto_preco.produto.nome} - {self.produto_preco.tamanho.nome}"

    def save(self, *args, **kwargs):
        # Se for meio a meio, recalcular preço
        if self.is_meio_a_meio:
            self.preco_unitario = self.calcular_preco_meio_a_meio()
        elif not self.preco_unitario:
            self.preco_unitario = self.produto_preco.preco_final
            
        self.subtotal = Decimal(str(self.quantidade)) * self.preco_unitario
        super().save(*args, **kwargs)
        # Note: calcular_total() should be called manually after all items are saved
        # to avoid circular references during bulk operations