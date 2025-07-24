from django.db import models
from django.core.validators import MinValueValidator

class UnidadeMedida(models.Model):
    nome = models.CharField(max_length=50)
    sigla = models.CharField(max_length=10, unique=True)
    
    class Meta:
        verbose_name = 'Unidade de Medida'
        verbose_name_plural = 'Unidades de Medida'
        ordering = ['nome']
    
    def __str__(self):
        return f"{self.nome} ({self.sigla})"

class Ingrediente(models.Model):
    nome = models.CharField(max_length=200)
    unidade_medida = models.ForeignKey(UnidadeMedida, on_delete=models.PROTECT)
    quantidade_estoque = models.DecimalField(
        max_digits=10, 
        decimal_places=3,
        default=0,
        validators=[MinValueValidator(0)]
    )
    estoque_minimo = models.DecimalField(
        max_digits=10, 
        decimal_places=3,
        default=0,
        validators=[MinValueValidator(0)]
    )
    custo_unitario = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)]
    )
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Ingrediente'
        verbose_name_plural = 'Ingredientes'
        ordering = ['nome']
    
    def __str__(self):
        return f"{self.nome} ({self.quantidade_estoque} {self.unidade_medida.sigla})"
    
    @property
    def estoque_baixo(self):
        return self.quantidade_estoque <= self.estoque_minimo

class MovimentoEstoque(models.Model):
    TIPO_CHOICES = [
        ('entrada', 'Entrada'),
        ('saida', 'Saída'),
        ('ajuste', 'Ajuste'),
        ('perda', 'Perda'),
    ]
    
    ingrediente = models.ForeignKey(Ingrediente, on_delete=models.CASCADE, related_name='movimentos')
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    quantidade = models.DecimalField(
        max_digits=10, 
        decimal_places=3,
        validators=[MinValueValidator(0)]
    )
    custo_unitario = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    custo_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    motivo = models.CharField(max_length=200)
    usuario = models.ForeignKey('auth.User', on_delete=models.PROTECT)
    data = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Movimento de Estoque'
        verbose_name_plural = 'Movimentos de Estoque'
        ordering = ['-data']
    
    def __str__(self):
        return f"{self.get_tipo_display()} - {self.ingrediente.nome} ({self.quantidade})"
    
    def save(self, *args, **kwargs):
        self.custo_total = self.quantidade * self.custo_unitario
        
        # Atualiza estoque do ingrediente
        if self.tipo in ['entrada', 'ajuste']:
            self.ingrediente.quantidade_estoque += self.quantidade
        elif self.tipo in ['saida', 'perda']:
            self.ingrediente.quantidade_estoque -= self.quantidade
        
        self.ingrediente.save()
        super().save(*args, **kwargs)

class ReceitaProduto(models.Model):
    """Relaciona produtos com ingredientes necessários"""
    produto = models.ForeignKey('produtos.Produto', on_delete=models.CASCADE, related_name='receitas')
    ingrediente = models.ForeignKey(Ingrediente, on_delete=models.CASCADE)
    quantidade = models.DecimalField(
        max_digits=10, 
        decimal_places=3,
        validators=[MinValueValidator(0)]
    )
    
    class Meta:
        verbose_name = 'Receita do Produto'
        verbose_name_plural = 'Receitas dos Produtos'
        unique_together = ['produto', 'ingrediente']
    
    def __str__(self):
        return f"{self.produto.nome} - {self.ingrediente.nome} ({self.quantidade})"