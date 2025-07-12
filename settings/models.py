from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

class UserPreference(models.Model):
    """
    Modelo para armazenar preferências do usuário, incluindo tema (dark mode)
    """
    THEME_CHOICES = [
        ('light', 'Claro'),
        ('dark', 'Escuro'),
        ('auto', 'Automático'),
    ]
    
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='preferences',
        verbose_name='Usuário'
    )
    
    theme = models.CharField(
        max_length=10,
        choices=THEME_CHOICES,
        default='auto',
        verbose_name='Tema',
        help_text='Preferência de tema da interface'
    )
    
    # Campos extras para futuras preferências
    notifications_enabled = models.BooleanField(
        default=True,
        verbose_name='Notificações ativadas'
    )
    
    language = models.CharField(
        max_length=10,
        default='pt-br',
        verbose_name='Idioma',
        validators=[RegexValidator(
            regex=r'^[a-z]{2}-[a-z]{2}$',
            message='Formato deve ser: pt-br, en-us, etc.'
        )]
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Criado em'
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Atualizado em'
    )
    
    class Meta:
        verbose_name = 'Preferência do Usuário'
        verbose_name_plural = 'Preferências dos Usuários'
    
    def __str__(self):
        return f'{self.user.username} - Tema: {self.get_theme_display()}'
    
    @classmethod
    def get_or_create_for_user(cls, user):
        """
        Método para obter ou criar preferências para um usuário
        """
        preference, created = cls.objects.get_or_create(
            user=user,
            defaults={'theme': 'auto'}
        )
        return preference
    
    def save(self, *args, **kwargs):
        """
        Override do save para validações adicionais
        """
        super().save(*args, **kwargs)
