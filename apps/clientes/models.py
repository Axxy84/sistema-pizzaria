from django.db import models
from django.core.validators import RegexValidator

phone_validator = RegexValidator(
    regex=r'^\+?1?\d{9,15}$',
    message="Número de telefone deve estar no formato: '+999999999'. Até 15 dígitos permitidos."
)

class Cliente(models.Model):
    nome = models.CharField(max_length=200)
    email = models.EmailField(blank=True)
    telefone = models.CharField(max_length=15, validators=[phone_validator])
    telefone2 = models.CharField(max_length=15, validators=[phone_validator], blank=True)
    cpf = models.CharField(max_length=14, blank=True, unique=True, null=True)
    data_nascimento = models.DateField(blank=True, null=True)
    observacoes = models.TextField(blank=True)
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['nome']
    
    def __str__(self):
        return f"{self.nome} - {self.telefone}"

class Endereco(models.Model):
    TIPO_CHOICES = [
        ('casa', 'Casa'),
        ('trabalho', 'Trabalho'),
        ('outro', 'Outro'),
    ]
    
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='enderecos')
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='casa')
    cep = models.CharField(max_length=9)
    logradouro = models.CharField(max_length=200)
    numero = models.CharField(max_length=20)
    complemento = models.CharField(max_length=100, blank=True)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2)
    referencia = models.CharField(max_length=200, blank=True)
    principal = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'Endereço'
        verbose_name_plural = 'Endereços'
        ordering = ['-principal', 'tipo']
    
    def __str__(self):
        return f"{self.logradouro}, {self.numero} - {self.bairro}"
    
    def save(self, *args, **kwargs):
        # Se for marcado como principal, desmarcar outros
        if self.principal:
            Endereco.objects.filter(
                cliente=self.cliente,
                principal=True
            ).exclude(pk=self.pk).update(principal=False)
        super().save(*args, **kwargs)