from django.db import models
from django.contrib.auth.models import User
from apps.clientes.models import Cliente, Endereco
from apps.produtos.models import Produto, ProdutoPreco
from decimal import Decimal

class Pedido(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('confirmado', 'Confirmado'),
        ('preparando', 'Preparando'),
        ('saiu_entrega', 'Saiu para Entrega'),
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
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
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
        return f"Pedido #{self.numero} - {self.cliente.nome}"
    
    def calcular_total(self):
        self.subtotal = sum(item.subtotal for item in self.itens.all())
        self.total = self.subtotal + self.taxa_entrega - self.desconto
        self.save()
    
    def save(self, *args, **kwargs):
        if not self.numero:
            # Gerar número do pedido
            ultimo = Pedido.objects.all().order_by('-id').first()
            if ultimo:
                self.numero = str(int(ultimo.numero) + 1).zfill(6)
            else:
                self.numero = '000001'
        super().save(*args, **kwargs)

class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='itens')
    produto_preco = models.ForeignKey(ProdutoPreco, on_delete=models.PROTECT)
    quantidade = models.IntegerField(default=1)
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    observacoes = models.TextField(blank=True)
    
    class Meta:
        verbose_name = 'Item do Pedido'
        verbose_name_plural = 'Itens do Pedido'
    
    def __str__(self):
        return f"{self.quantidade}x {self.produto_preco.produto.nome}"
    
    def save(self, *args, **kwargs):
        if not self.preco_unitario:
            self.preco_unitario = self.produto_preco.preco_final
        self.subtotal = Decimal(str(self.quantidade)) * self.preco_unitario
        super().save(*args, **kwargs)
        self.pedido.calcular_total()