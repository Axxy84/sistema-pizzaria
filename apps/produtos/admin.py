from django.contrib import admin
from .models import Categoria, Tamanho, Produto, ProdutoPreco

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'ativo', 'criado_em']
    list_filter = ['ativo', 'criado_em']
    search_fields = ['nome', 'descricao']
    ordering = ['nome']

@admin.register(Tamanho)
class TamanhoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'ordem', 'ativo']
    list_filter = ['ativo']
    ordering = ['ordem', 'nome']

class ProdutoPrecoInline(admin.TabularInline):
    model = ProdutoPreco
    extra = 1
    fields = ['tamanho', 'preco', 'preco_promocional']

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'categoria', 'ativo', 'criado_em']
    list_filter = ['categoria', 'ativo', 'criado_em']
    search_fields = ['nome', 'descricao']
    ordering = ['categoria', 'nome']
    inlines = [ProdutoPrecoInline]
    
    fieldsets = (
        (None, {
            'fields': ('nome', 'categoria', 'descricao')
        }),
        ('Mídia', {
            'fields': ('imagem',)
        }),
        ('Status', {
            'fields': ('ativo',)
        }),
    )