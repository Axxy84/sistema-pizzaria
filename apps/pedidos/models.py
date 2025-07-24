from django.db import models
from apps.clientes.models import Cliente, Endereco
from apps.produtos.models import Produto, ProdutoPreco
from decimal import Decimal
import json
from .models_mesa import Mesa
from .models_config import ConfiguracaoPedido

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
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name='pedidos', null=True, blank=True)
    usuario = models.ForeignKey('auth.User', on_delete=models.PROTECT, related_name='pedidos_atendidos')
    
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
    
    # Novo campo para número da mesa
    mesa_numero = models.CharField(max_length=10, blank=True, help_text='Número da mesa para pedidos de mesa')
    
    # Campos de status baseados em timestamp
    cancelado_em = models.DateTimeField(null=True, blank=True)
    entregue_em = models.DateTimeField(null=True, blank=True)
    motivo_cancelamento = models.TextField(blank=True)
    preparacao_iniciada_em = models.DateTimeField(null=True, blank=True)
    saida_confirmada_em = models.DateTimeField(null=True, blank=True)
    
    @property
    def tempo_desde_criacao(self):
        """Retorna o tempo decorrido desde a criação do pedido"""
        from django.utils import timezone
        delta = timezone.now() - self.criado_em
        
        if delta.days > 0:
            return f"{delta.days} dia{'s' if delta.days > 1 else ''}"
        
        hours = delta.seconds // 3600
        if hours > 0:
            return f"{hours} hora{'s' if hours > 1 else ''}"
        
        minutes = (delta.seconds % 3600) // 60
        return f"{minutes} minuto{'s' if minutes != 1 else ''}"
    
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
        if self.is_meio_a_meio and self.meio_a_meio_data:
            # Tenta com underscore primeiro, depois sem
            return self.meio_a_meio_data.get('sabor_1') or self.meio_a_meio_data.get('sabor1')
        return None
    
    @property
    def sabor_2(self):
        """Retorna dados do segundo sabor se for meio a meio"""
        if self.is_meio_a_meio and self.meio_a_meio_data:
            # Tenta com underscore primeiro, depois sem
            return self.meio_a_meio_data.get('sabor_2') or self.meio_a_meio_data.get('sabor2')
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
        if not self.is_meio_a_meio or not self.meio_a_meio_data:
            return self.preco_unitario or Decimal('0')
        
        # Se sabor_1 ou sabor_2 forem strings (nomes), usar o preço direto do meio_a_meio_data
        if isinstance(self.sabor_1, str) or isinstance(self.sabor_2, str):
            # Pegar o preço direto do meio_a_meio_data
            preco = self.meio_a_meio_data.get('preco', 0)
            return Decimal(str(preco))
        
        # Se forem dicionários com informações completas
        sabor_1_data = self.sabor_1 if isinstance(self.sabor_1, dict) else {}
        sabor_2_data = self.sabor_2 if isinstance(self.sabor_2, dict) else {}
        
        sabor_1_preco = Decimal(str(sabor_1_data.get('preco', 0)))
        sabor_2_preco = Decimal(str(sabor_2_data.get('preco', 0)))
        regra = self.meio_a_meio_data.get('regra_preco', 'mais_caro')
        
        if regra == 'mais_caro':
            return max(sabor_1_preco, sabor_2_preco)
        elif regra == 'media':
            return (sabor_1_preco + sabor_2_preco) / 2
        else:
            return self.preco_unitario or Decimal('0')
    
    def get_descricao_completa(self):
        """Retorna descrição completa do item, incluindo meio a meio"""
        if self.is_meio_a_meio and self.meio_a_meio_data:
            # Se sabor_1 e sabor_2 forem strings diretos
            if isinstance(self.sabor_1, str):
                sabor_1_nome = self.sabor_1
            elif isinstance(self.sabor_1, dict):
                sabor_1_nome = self.sabor_1.get('nome', 'Sabor 1')
            else:
                sabor_1_nome = 'Sabor 1'
                
            if isinstance(self.sabor_2, str):
                sabor_2_nome = self.sabor_2
            elif isinstance(self.sabor_2, dict):
                sabor_2_nome = self.sabor_2.get('nome', 'Sabor 2')
            else:
                sabor_2_nome = 'Sabor 2'
                
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