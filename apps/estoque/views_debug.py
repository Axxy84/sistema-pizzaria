"""
Views de debug para o estoque - SEM autenticação obrigatória
Apenas para testes durante desenvolvimento
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, F
from django.http import JsonResponse
from .models import Ingrediente, MovimentoEstoque, UnidadeMedida, ReceitaProduto
from .forms import IngredienteForm, MovimentoEstoqueForm

def estoque_dashboard_debug(request):
    """Dashboard principal do estoque - VERSÃO DEBUG SEM LOGIN"""
    # Estatísticas gerais
    total_ingredientes = Ingrediente.objects.filter(ativo=True).count()
    ingredientes_estoque_baixo = Ingrediente.objects.filter(
        quantidade_estoque__lte=F('estoque_minimo'),
        ativo=True
    ).count()
    
    # Ingredientes com estoque baixo
    ingredientes_baixo = Ingrediente.objects.filter(
        quantidade_estoque__lte=F('estoque_minimo'),
        ativo=True
    ).select_related('unidade_medida')[:5]
    
    # Últimos movimentos
    ultimos_movimentos = MovimentoEstoque.objects.select_related(
        'ingrediente', 'usuario'
    ).order_by('-data')[:10]
    
    # Valor total do estoque
    valor_total_estoque = sum(
        ing.quantidade_estoque * ing.custo_unitario 
        for ing in Ingrediente.objects.filter(ativo=True)
    )
    
    context = {
        'total_ingredientes': total_ingredientes,
        'ingredientes_estoque_baixo': ingredientes_estoque_baixo,
        'ingredientes_baixo': ingredientes_baixo,
        'ultimos_movimentos': ultimos_movimentos,
        'valor_total_estoque': valor_total_estoque,
        'debug_mode': True,
    }
    
    return render(request, 'estoque/dashboard.html', context)

def ingrediente_list_debug(request):
    """Lista todos os ingredientes - VERSÃO DEBUG SEM LOGIN"""
    search = request.GET.get('search', '')
    status_filter = request.GET.get('status', 'todos')
    estoque_filter = request.GET.get('estoque', 'todos')
    
    ingredients = Ingrediente.objects.select_related('unidade_medida')
    
    if search:
        ingredients = ingredients.filter(
            Q(nome__icontains=search)
        )
    
    if status_filter == 'ativo':
        ingredients = ingredients.filter(ativo=True)
    elif status_filter == 'inativo':
        ingredients = ingredients.filter(ativo=False)
    
    if estoque_filter == 'baixo':
        ingredients = ingredients.filter(quantidade_estoque__lte=F('estoque_minimo'))
    elif estoque_filter == 'zerado':
        ingredients = ingredients.filter(quantidade_estoque=0)
    
    ingredients = ingredients.order_by('nome')
    
    paginator = Paginator(ingredients, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search': search,
        'status_filter': status_filter,
        'estoque_filter': estoque_filter,
        'debug_mode': True,
    }
    
    return render(request, 'estoque/ingrediente_list.html', context)

def ingrediente_detail_debug(request, pk):
    """Detalhes de um ingrediente - VERSÃO DEBUG SEM LOGIN"""
    ingrediente = get_object_or_404(Ingrediente, pk=pk)
    
    # Histórico de movimentos
    movimentos = MovimentoEstoque.objects.filter(
        ingrediente=ingrediente
    ).select_related('usuario').order_by('-data')
    
    paginator = Paginator(movimentos, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Receitas que usam este ingrediente
    receitas = ReceitaProduto.objects.filter(
        ingrediente=ingrediente
    ).select_related('produto')
    
    context = {
        'ingrediente': ingrediente,
        'page_obj': page_obj,
        'receitas': receitas,
        'debug_mode': True,
    }
    
    return render(request, 'estoque/ingrediente_detail.html', context)

def movimento_list_debug(request):
    """Lista movimentos de estoque - VERSÃO DEBUG SEM LOGIN"""
    search = request.GET.get('search', '')
    tipo_filter = request.GET.get('tipo', 'todos')
    ingrediente_filter = request.GET.get('ingrediente', '')
    
    movimentos = MovimentoEstoque.objects.select_related(
        'ingrediente', 'usuario'
    )
    
    if search:
        movimentos = movimentos.filter(
            Q(ingrediente__nome__icontains=search) |
            Q(motivo__icontains=search)
        )
    
    if tipo_filter != 'todos':
        movimentos = movimentos.filter(tipo=tipo_filter)
    
    if ingrediente_filter:
        movimentos = movimentos.filter(ingrediente_id=ingrediente_filter)
    
    movimentos = movimentos.order_by('-data')
    
    paginator = Paginator(movimentos, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Para o filtro de ingredientes
    ingredientes = Ingrediente.objects.filter(ativo=True).order_by('nome')
    
    context = {
        'page_obj': page_obj,
        'search': search,
        'tipo_filter': tipo_filter,
        'ingrediente_filter': ingrediente_filter,
        'ingredientes': ingredientes,
        'tipo_choices': MovimentoEstoque.TIPO_CHOICES,
        'debug_mode': True,
    }
    
    return render(request, 'estoque/movimento_list.html', context)

def estoque_baixo_debug(request):
    """Lista ingredientes com estoque baixo - VERSÃO DEBUG SEM LOGIN"""
    ingredientes = Ingrediente.objects.filter(
        quantidade_estoque__lte=F('estoque_minimo'),
        ativo=True
    ).select_related('unidade_medida').order_by('quantidade_estoque')
    
    context = {
        'ingredientes': ingredientes,
        'debug_mode': True,
    }
    return render(request, 'estoque/estoque_baixo.html', context)