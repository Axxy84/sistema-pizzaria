from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, F
from django.http import JsonResponse
from .models import Ingrediente, MovimentoEstoque, UnidadeMedida, ReceitaProduto
from .forms import IngredienteForm, MovimentoEstoqueForm

def estoque_dashboard(request):
    """Dashboard principal do estoque"""
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
    }
    
    return render(request, 'estoque/dashboard.html', context)

def ingrediente_list(request):
    """Lista todos os ingredientes"""
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
    }
    
    return render(request, 'estoque/ingrediente_list.html', context)

def ingrediente_detail(request, pk):
    """Detalhes de um ingrediente"""
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
    }
    
    return render(request, 'estoque/ingrediente_detail.html', context)

def ingrediente_create(request):
    """Criar novo ingrediente"""
    if request.method == 'POST':
        form = IngredienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ingrediente criado com sucesso!')
            return redirect('estoque:ingrediente_list')
    else:
        form = IngredienteForm()
    
    context = {'form': form, 'title': 'Criar Ingrediente'}
    return render(request, 'estoque/ingrediente_form.html', context)

def ingrediente_edit(request, pk):
    """Editar ingrediente"""
    ingrediente = get_object_or_404(Ingrediente, pk=pk)
    
    if request.method == 'POST':
        form = IngredienteForm(request.POST, instance=ingrediente)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ingrediente atualizado com sucesso!')
            return redirect('estoque:ingrediente_detail', pk=pk)
    else:
        form = IngredienteForm(instance=ingrediente)
    
    context = {
        'form': form, 
        'ingrediente': ingrediente,
        'title': 'Editar Ingrediente'
    }
    return render(request, 'estoque/ingrediente_form.html', context)

def movimento_list(request):
    """Lista movimentos de estoque"""
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
    }
    
    return render(request, 'estoque/movimento_list.html', context)

def movimento_create(request):
    """Criar movimento de estoque"""
    if request.method == 'POST':
        form = MovimentoEstoqueForm(request.POST)
        if form.is_valid():
            movimento = form.save(commit=False)
            movimento.usuario = request.user
            
            # Validar estoque suficiente para saída/perda
            if movimento.tipo in ['saida', 'perda']:
                if movimento.ingrediente.quantidade_estoque < movimento.quantidade:
                    messages.error(
                        request, 
                        f'Estoque insuficiente! Disponível: {movimento.ingrediente.quantidade_estoque}'
                    )
                    context = {'form': form, 'title': 'Novo Movimento'}
                    return render(request, 'estoque/movimento_form.html', context)
            
            movimento.save()
            messages.success(request, 'Movimento registrado com sucesso!')
            return redirect('estoque:movimento_list')
    else:
        form = MovimentoEstoqueForm()
    
    context = {'form': form, 'title': 'Novo Movimento'}
    return render(request, 'estoque/movimento_form.html', context)

def estoque_baixo(request):
    """Lista ingredientes com estoque baixo"""
    ingredientes = Ingrediente.objects.filter(
        quantidade_estoque__lte=F('estoque_minimo'),
        ativo=True
    ).select_related('unidade_medida').order_by('quantidade_estoque')
    
    context = {'ingredientes': ingredientes}
    return render(request, 'estoque/estoque_baixo.html', context)

def relatorio_movimentos(request):
    """Relatório de movimentos por período"""
    from django.utils import timezone
    from datetime import datetime, timedelta
    
    # Parâmetros de filtro
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')
    tipo_filter = request.GET.get('tipo', 'todos')
    
    # Definir período padrão (último mês)
    if not data_inicio:
        data_inicio = (timezone.now() - timedelta(days=30)).date()
    else:
        data_inicio = datetime.strptime(data_inicio, '%Y-%m-%d').date()
    
    if not data_fim:
        data_fim = timezone.now().date()
    else:
        data_fim = datetime.strptime(data_fim, '%Y-%m-%d').date()
    
    # Filtrar movimentos
    movimentos = MovimentoEstoque.objects.filter(
        data__date__gte=data_inicio,
        data__date__lte=data_fim
    ).select_related('ingrediente', 'usuario')
    
    if tipo_filter != 'todos':
        movimentos = movimentos.filter(tipo=tipo_filter)
    
    # Calcular totais por tipo
    totais = {}
    for tipo, _ in MovimentoEstoque.TIPO_CHOICES:
        tipo_movimentos = movimentos.filter(tipo=tipo)
        totais[tipo] = {
            'quantidade': sum(m.quantidade for m in tipo_movimentos),
            'valor': sum(m.custo_total for m in tipo_movimentos),
            'count': tipo_movimentos.count()
        }
    
    context = {
        'movimentos': movimentos.order_by('-data'),
        'data_inicio': data_inicio,
        'data_fim': data_fim,
        'tipo_filter': tipo_filter,
        'totais': totais,
        'tipo_choices': MovimentoEstoque.TIPO_CHOICES,
    }
    
    return render(request, 'estoque/relatorio_movimentos.html', context)

def ingrediente_ajax_search(request):
    """Busca AJAX para ingredientes"""
    term = request.GET.get('term', '')
    ingredientes = Ingrediente.objects.filter(
        nome__icontains=term,
        ativo=True
    )[:10]
    
    results = []
    for ing in ingredientes:
        results.append({
            'id': ing.id,
            'label': f"{ing.nome} ({ing.quantidade_estoque} {ing.unidade_medida.sigla})",
            'value': ing.nome,
            'estoque': float(ing.quantidade_estoque),
            'unidade': ing.unidade_medida.sigla
        })
    
    return JsonResponse(results, safe=False)