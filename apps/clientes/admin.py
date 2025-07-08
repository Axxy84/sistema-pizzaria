from django.contrib import admin
from .models import Cliente, Endereco

class EnderecoInline(admin.StackedInline):
    model = Endereco
    extra = 0
    fields = [
        'tipo', 'principal', 
        ('cep', 'logradouro', 'numero'),
        ('complemento', 'bairro'),
        ('cidade', 'estado'),
        'referencia'
    ]

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['nome', 'telefone', 'email', 'ativo', 'criado_em']
    list_filter = ['ativo', 'criado_em']
    search_fields = ['nome', 'telefone', 'email', 'cpf']
    ordering = ['nome']
    inlines = [EnderecoInline]
    
    fieldsets = (
        ('Informações Pessoais', {
            'fields': ('nome', 'cpf', 'data_nascimento')
        }),
        ('Contato', {
            'fields': ('telefone', 'telefone2', 'email')
        }),
        ('Outros', {
            'fields': ('observacoes', 'ativo')
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editando
            return ['cpf']
        return []