from django import template

register = template.Library()

@register.filter
def get_preco_tamanho(pizza, tamanho):
    """Retorna o preço de uma pizza para um tamanho específico"""
    for preco in pizza.precos.all():
        if preco.tamanho.id == tamanho.id:
            return preco.preco_final
    return None