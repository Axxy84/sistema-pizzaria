from django.db import models
from django.contrib.auth.hashers import make_password, check_password


class ConfiguracaoPedido(models.Model):
    """Configurações gerais do sistema de pedidos"""
    
    # Senha de cancelamento (armazenada com hash)
    senha_cancelamento_hash = models.CharField(
        max_length=256, 
        default='',
        help_text='Senha necessária para cancelar pedidos (armazenada com hash)'
    )
    
    # Outras configurações podem ser adicionadas aqui
    permitir_cancelamento = models.BooleanField(
        default=True,
        help_text='Permite cancelamento de pedidos'
    )
    
    tempo_maximo_cancelamento = models.IntegerField(
        default=30,
        help_text='Tempo máximo em minutos para cancelar um pedido após criação'
    )
    
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Configuração de Pedidos'
        verbose_name_plural = 'Configurações de Pedidos'
    
    def __str__(self):
        return f"Configuração de Pedidos (Atualizada em {self.atualizado_em.strftime('%d/%m/%Y %H:%M')})"
    
    def set_senha_cancelamento(self, senha_raw):
        """Define a senha de cancelamento (com hash)"""
        self.senha_cancelamento_hash = make_password(senha_raw)
        self.save()
    
    def check_senha_cancelamento(self, senha_raw):
        """Verifica se a senha está correta"""
        if not self.senha_cancelamento_hash:
            # Se não há senha definida, usar a padrão
            return senha_raw == 'admin123'
        return check_password(senha_raw, self.senha_cancelamento_hash)
    
    @classmethod
    def get_configuracao(cls):
        """Retorna a configuração única ou cria uma nova"""
        config, created = cls.objects.get_or_create(pk=1)
        if created:
            # Definir senha padrão na primeira vez
            config.set_senha_cancelamento('admin123')
        return config