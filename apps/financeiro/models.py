from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal

class Caixa(models.Model):
    STATUS_CHOICES = [
        ('aberto', 'Aberto'),
        ('fechado', 'Fechado'),
    ]
    
    usuario = models.ForeignKey(User, on_delete=models.PROTECT, related_name='caixas')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='aberto')
    valor_abertura = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    valor_fechamento = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        null=True,
        blank=True
    )
    data_abertura = models.DateTimeField(auto_now_add=True)
    data_fechamento = models.DateTimeField(null=True, blank=True)
    observacoes_abertura = models.TextField(blank=True)
    observacoes_fechamento = models.TextField(blank=True)
    
    class Meta:
        verbose_name = 'Caixa'
        verbose_name_plural = 'Caixas'
        ordering = ['-data_abertura']
    
    def __str__(self):
        return f"Caixa {self.data_abertura.strftime('%d/%m/%Y')} - {self.usuario.username}"
    
    @property
    def saldo_esperado(self):
        total_entradas = self.movimentos.filter(tipo='entrada').aggregate(
            total=models.Sum('valor')
        )['total'] or Decimal('0')
        
        total_saidas = self.movimentos.filter(tipo='saida').aggregate(
            total=models.Sum('valor')
        )['total'] or Decimal('0')
        
        return self.valor_abertura + total_entradas - total_saidas
    
    @property
    def diferenca(self):
        if self.valor_fechamento:
            return self.valor_fechamento - self.saldo_esperado
        return None

class MovimentoCaixa(models.Model):
    TIPO_CHOICES = [
        ('entrada', 'Entrada'),
        ('saida', 'Saída'),
    ]
    
    CATEGORIA_CHOICES = [
        ('venda', 'Venda'),
        ('sangria', 'Sangria'),
        ('suprimento', 'Suprimento'),
        ('despesa', 'Despesa'),
        ('outros', 'Outros'),
    ]
    
    caixa = models.ForeignKey(Caixa, on_delete=models.CASCADE, related_name='movimentos')
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    categoria = models.CharField(max_length=20, choices=CATEGORIA_CHOICES)
    descricao = models.CharField(max_length=200)
    valor = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    pedido = models.ForeignKey(
        'pedidos.Pedido', 
        on_delete=models.PROTECT, 
        null=True, 
        blank=True,
        related_name='movimentos_caixa'
    )
    usuario = models.ForeignKey(User, on_delete=models.PROTECT)
    data = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Movimento de Caixa'
        verbose_name_plural = 'Movimentos de Caixa'
        ordering = ['-data']
    
    def __str__(self):
        return f"{self.get_tipo_display()} - {self.descricao} - R$ {self.valor}"

class ContaPagar(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('pago', 'Pago'),
        ('cancelado', 'Cancelado'),
    ]
    
    CATEGORIA_CHOICES = [
        ('fornecedor', 'Fornecedor'),
        ('funcionario', 'Funcionário'),
        ('aluguel', 'Aluguel'),
        ('energia', 'Energia'),
        ('agua', 'Água'),
        ('internet', 'Internet'),
        ('outros', 'Outros'),
    ]
    
    descricao = models.CharField(max_length=200)
    categoria = models.CharField(max_length=20, choices=CATEGORIA_CHOICES)
    valor = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    data_vencimento = models.DateField()
    data_pagamento = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
    observacoes = models.TextField(blank=True)
    criado_por = models.ForeignKey(User, on_delete=models.PROTECT, related_name='contas_criadas')
    pago_por = models.ForeignKey(
        User, 
        on_delete=models.PROTECT, 
        null=True, 
        blank=True,
        related_name='contas_pagas'
    )
    criado_em = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Conta a Pagar'
        verbose_name_plural = 'Contas a Pagar'
        ordering = ['status', 'data_vencimento']
    
    def __str__(self):
        return f"{self.descricao} - R$ {self.valor} - {self.data_vencimento}"
    
    @property
    def vencida(self):
        from datetime import date
        return self.status == 'pendente' and self.data_vencimento < date.today()