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
    nome = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name='produtos')
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