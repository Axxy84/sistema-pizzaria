from django.db import models
from django.core.validators import MinValueValidator

class Categoria(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    descricao = models.TextField(blank=True)
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['nome']
    
    def __str__(self):
        return self.nome

class Tamanho(models.Model):
    nome = models.CharField(max_length=50, unique=True)
    ordem = models.IntegerField(default=0)
    ativo = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Tamanho'
        verbose_name_plural = 'Tamanhos'
        ordering = ['ordem', 'nome']
    
    def __str__(self):
        return self.nome

class Produto(models.Model):
    TIPO_CHOICES = [
        ('pizza', 'Pizza'),
        ('bebida', 'Bebida'),
        ('borda', 'Borda Recheada'),
        ('sobremesa', 'Sobremesa'),
        ('acompanhamento', 'Acompanhamento'),
        ('outro', 'Outro'),
    ]
    
    nome = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name='produtos')
    tipo_produto = models.CharField(max_length=50, choices=TIPO_CHOICES, default='outro')
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True,
                                        help_text="Preço único para produtos sem variação de tamanho")
    tamanhos_precos = models.JSONField(null=True, blank=True,
                                       help_text="JSON com tamanhos e preços para produtos com variações")
    ingredientes = models.TextField(null=True, blank=True,
                                   help_text="Lista de ingredientes separados por vírgula")
    estoque_disponivel = models.IntegerField(default=0,
                                           help_text="Quantidade em estoque (0 = sem controle)")
    imagem = models.ImageField(upload_to='produtos/', blank=True, null=True)
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'
        ordering = ['categoria', 'nome']
    
    def __str__(self):
        return f"{self.nome} ({self.categoria})"
    
    @property
    def tem_tamanhos(self):
        return self.precos.exists() or bool(self.tamanhos_precos)
    
    @property
    def preco_display(self):
        if self.preco_unitario:
            return f"R$ {self.preco_unitario}"
        elif self.precos.exists():
            menor_preco = self.precos.order_by('preco').first()
            if menor_preco:
                return f"A partir de R$ {menor_preco.preco_final}"
        return "Sob consulta"
    
    def get_tipo_display_badge(self):
        cores = {
            'pizza': 'bg-red-100 text-red-800',
            'bebida': 'bg-blue-100 text-blue-800',
            'borda': 'bg-yellow-100 text-yellow-800',
            'sobremesa': 'bg-purple-100 text-purple-800',
            'acompanhamento': 'bg-green-100 text-green-800',
            'outro': 'bg-gray-100 text-gray-800',
        }
        return cores.get(self.tipo_produto, cores['outro'])
    
    def get_preco_por_tamanho(self, tamanho_id):
        """Retorna o preço para um tamanho específico"""
        preco = self.precos.filter(tamanho_id=tamanho_id).first()
        return preco.preco_final if preco else None

class ProdutoPreco(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name='precos')
    tamanho = models.ForeignKey(Tamanho, on_delete=models.PROTECT)
    preco = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    preco_promocional = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0)],
        blank=True,
        null=True
    )
    
    class Meta:
        verbose_name = 'Preço do Produto'
        verbose_name_plural = 'Preços dos Produtos'
        unique_together = ['produto', 'tamanho']
    
    def __str__(self):
        return f"{self.produto.nome} - {self.tamanho.nome}: R$ {self.preco}"
    
    @property
    def preco_final(self):
        return self.preco_promocional or self.preco