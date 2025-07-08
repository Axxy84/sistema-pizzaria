from django.contrib import admin
from .models import Pedido, ItemPedido

class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 0
    readonly_fields = ['preco_unitario', 'subtotal']
    fields = ['produto_preco', 'quantidade', 'preco_unitario', 'subtotal', 'observacoes']

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = [
        'numero', 'cliente', 'tipo', 'status', 
        'total', 'forma_pagamento', 'criado_em'
    ]
    list_filter = ['status', 'tipo', 'forma_pagamento', 'criado_em']
    search_fields = ['numero', 'cliente__nome', 'cliente__telefone']
    ordering = ['-criado_em']
    readonly_fields = ['numero', 'subtotal', 'total', 'criado_em', 'atualizado_em']
    inlines = [ItemPedidoInline]
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('numero', 'cliente', 'usuario', 'tipo')
        }),
        ('Entrega', {
            'fields': ('endereco_entrega', 'mesa'),
            'classes': ('collapse',)
        }),
        ('Pagamento', {
            'fields': (
                'forma_pagamento', 'precisa_troco', 'troco_para',
                'subtotal', 'taxa_entrega', 'desconto', 'total'
            )
        }),
        ('Status', {
            'fields': ('status', 'observacoes')
        }),
        ('Datas', {
            'fields': ('criado_em', 'atualizado_em'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:  # Novo pedido
            obj.usuario = request.user
        super().save_model(request, obj, form, change)
    
    def save_formset(self, request, form, formset, change):
        super().save_formset(request, form, formset, change)
        # Recalcula o total após salvar os itens
        form.instance.calcular_total()