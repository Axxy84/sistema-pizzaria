from django.db import models
from django.utils import timezone
from decimal import Decimal

class Mesa(models.Model):
    """
    Modelo para gerenciar mesas abertas no restaurante
    """
    STATUS_CHOICES = [
        ('aberta', 'Aberta'),
        ('fechada', 'Fechada'),
        ('reservada', 'Reservada'),
    ]
    
    numero = models.CharField(max_length=10, unique=True, verbose_name='Número da Mesa')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='aberta')
    
    # Timestamps
    aberta_em = models.DateTimeField(default=timezone.now, verbose_name='Aberta em')
    fechada_em = models.DateTimeField(null=True, blank=True, verbose_name='Fechada em')
    
    # Valores
    total_consumido = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Total Consumido')
    
    # Pessoa responsável
    responsavel = models.CharField(max_length=100, blank=True, verbose_name='Responsável pela Mesa')
    
    class Meta:
        verbose_name = 'Mesa'
        verbose_name_plural = 'Mesas'
        ordering = ['numero']
    
    def __str__(self):
        return f"Mesa {self.numero} - {self.get_status_display()}"
    
    @property
    def tempo_aberta(self):
        """Retorna o tempo que a mesa está aberta"""
        if self.status != 'aberta':
            return None
            
        delta = timezone.now() - self.aberta_em
        hours = delta.seconds // 3600
        minutes = (delta.seconds % 3600) // 60
        
        if delta.days > 0:
            return f"{delta.days} dia{'s' if delta.days > 1 else ''}, {hours}h{minutes}min"
        elif hours > 0:
            return f"{hours}h{minutes}min"
        else:
            return f"{minutes} minuto{'s' if minutes != 1 else ''}"
    
    @property
    def pedidos_ativos(self):
        """Retorna todos os pedidos ativos da mesa"""
        from .models import Pedido
        return Pedido.objects.filter(
            tipo='mesa',
            mesa_numero=self.numero,
            status__in=['recebido', 'preparando', 'saindo']
        ).order_by('-criado_em')
    
    @property
    def total_pedidos(self):
        """Calcula o total de todos os pedidos da mesa"""
        total = self.pedidos_ativos.aggregate(
            total=models.Sum('total')
        )['total'] or Decimal('0')
        return total
    
    def fechar_mesa(self):
        """Fecha a mesa e marca todos os pedidos como entregues"""
        self.status = 'fechada'
        self.fechada_em = timezone.now()
        self.total_consumido = self.total_pedidos
        self.save()
        
        # Marcar todos os pedidos como entregues
        self.pedidos_ativos.update(status='entregue')
    
    def reabrir_mesa(self):
        """Reabre uma mesa fechada"""
        self.status = 'aberta'
        self.fechada_em = None
        self.aberta_em = timezone.now()
        self.total_consumido = Decimal('0')
        self.responsavel = ''
        self.save()
    
    def get_comanda_completa(self):
        """Retorna todos os itens consumidos na mesa para impressão"""
        from .models import Pedido
        pedidos = Pedido.objects.filter(
            tipo='mesa',
            mesa_numero=self.numero
        ).prefetch_related('itens__produto_preco__produto').order_by('criado_em')
        
        return {
            'mesa': self,
            'pedidos': pedidos,
            'total': self.total_pedidos,
            'tempo_aberta': self.tempo_aberta
        }