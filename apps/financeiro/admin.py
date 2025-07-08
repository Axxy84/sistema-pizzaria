from django.contrib import admin
from .models import Caixa, MovimentoCaixa, ContaPagar

@admin.register(Caixa)
class CaixaAdmin(admin.ModelAdmin):
    list_display = [
        'data_abertura', 'usuario', 'status',
        'valor_abertura', 'valor_fechamento', 'diferenca'
    ]
    list_filter = ['status', 'data_abertura']
    search_fields = ['usuario__username']
    ordering = ['-data_abertura']
    readonly_fields = [
        'data_abertura', 'data_fechamento', 'saldo_esperado', 'diferenca'
    ]
    
    fieldsets = (
        ('Abertura', {
            'fields': (
                'usuario', 'data_abertura', 'valor_abertura',
                'observacoes_abertura'
            )
        }),
        ('Fechamento', {
            'fields': (
                'status', 'data_fechamento', 'valor_fechamento',
                'observacoes_fechamento'
            )
        }),
        ('Resumo', {
            'fields': ('saldo_esperado', 'diferenca'),
            'classes': ('collapse',)
        }),
    )
    
    def has_delete_permission(self, request, obj=None):
        # Não permite deletar caixas
        return False

@admin.register(MovimentoCaixa)
class MovimentoCaixaAdmin(admin.ModelAdmin):
    list_display = [
        'data', 'tipo', 'categoria', 'descricao',
        'valor', 'caixa', 'usuario'
    ]
    list_filter = ['tipo', 'categoria', 'data']
    search_fields = ['descricao']
    ordering = ['-data']
    readonly_fields = ['data', 'usuario']
    
    fieldsets = (
        (None, {
            'fields': ('caixa', 'tipo', 'categoria')
        }),
        ('Detalhes', {
            'fields': ('descricao', 'valor', 'pedido')
        }),
        ('Informações', {
            'fields': ('usuario', 'data'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.usuario = request.user
        super().save_model(request, obj, form, change)

@admin.register(ContaPagar)
class ContaPagarAdmin(admin.ModelAdmin):
    list_display = [
        'descricao', 'categoria', 'valor',
        'data_vencimento', 'status', 'vencida'
    ]
    list_filter = ['status', 'categoria', 'data_vencimento']
    search_fields = ['descricao']
    ordering = ['status', 'data_vencimento']
    readonly_fields = ['criado_por', 'pago_por', 'criado_em', 'vencida']
    
    fieldsets = (
        (None, {
            'fields': ('descricao', 'categoria', 'valor')
        }),
        ('Datas', {
            'fields': ('data_vencimento', 'data_pagamento')
        }),
        ('Status', {
            'fields': ('status', 'vencida', 'observacoes')
        }),
        ('Informações', {
            'fields': ('criado_por', 'pago_por', 'criado_em'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.criado_por = request.user
        super().save_model(request, obj, form, change)