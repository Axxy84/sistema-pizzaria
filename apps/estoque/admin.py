from django.contrib import admin
from .models import UnidadeMedida, Ingrediente, MovimentoEstoque, ReceitaProduto

@admin.register(UnidadeMedida)
class UnidadeMedidaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'sigla']
    search_fields = ['nome', 'sigla']
    ordering = ['nome']

@admin.register(Ingrediente)
class IngredienteAdmin(admin.ModelAdmin):
    list_display = [
        'nome', 'quantidade_estoque', 'unidade_medida',
        'estoque_minimo', 'custo_unitario', 'ativo'
    ]
    list_filter = ['ativo', 'unidade_medida']
    search_fields = ['nome']
    ordering = ['nome']
    
    def get_list_display(self, request):
        # Adiciona indicador visual para estoque baixo
        list_display = super().get_list_display(request)
        
        def estoque_status(obj):
            if obj.estoque_baixo:
                return '⚠️ Baixo'
            return '✅ OK'
        estoque_status.short_description = 'Status'
        
        return list(list_display) + [estoque_status]

@admin.register(MovimentoEstoque)
class MovimentoEstoqueAdmin(admin.ModelAdmin):
    list_display = [
        'data', 'ingrediente', 'tipo', 'quantidade',
        'custo_total', 'usuario'
    ]
    list_filter = ['tipo', 'data', 'ingrediente']
    search_fields = ['ingrediente__nome', 'motivo']
    ordering = ['-data']
    readonly_fields = ['custo_total', 'data', 'usuario']
    
    fieldsets = (
        (None, {
            'fields': ('ingrediente', 'tipo', 'quantidade', 'custo_unitario')
        }),
        ('Informações', {
            'fields': ('motivo', 'custo_total', 'usuario', 'data')
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.usuario = request.user
        super().save_model(request, obj, form, change)

@admin.register(ReceitaProduto)
class ReceitaProdutoAdmin(admin.ModelAdmin):
    list_display = ['produto', 'ingrediente', 'quantidade']
    list_filter = ['produto__categoria']
    search_fields = ['produto__nome', 'ingrediente__nome']
    ordering = ['produto__nome', 'ingrediente__nome']