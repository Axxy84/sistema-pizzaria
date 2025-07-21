from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from apps.produtos.models import Produto
from apps.clientes.models import Cliente
from apps.pedidos.models import Pedido
from apps.financeiro.models import MovimentoCaixa
from django.db.models import Count, Sum
from django.utils import timezone
from datetime import datetime, timedelta
import json

def home_view(request):
    """
    View principal do dashboard com dados e gráficos
    """
    print(f"DEBUG HOME VIEW: User = {request.user}, Authenticated = {request.user.is_authenticated}")
    
    context = {
        'user': request.user,  # Garante que o usuário está no contexto
        'debug_info': {
            'user_id': request.user.id if request.user.is_authenticated else None,
            'username': request.user.username if request.user.is_authenticated else None,
            'is_authenticated': request.user.is_authenticated,
            'session_key': request.session.session_key,
        }
    }
    
    # Se usuário estiver logado, adiciona dados do dashboard
    if request.user.is_authenticated:
        # Estatísticas básicas
        pedidos_hoje_count = Pedido.objects.filter(
            criado_em__date=timezone.now().date()
        ).count()
        
        # Calcular faturamento hoje (pedidos não cancelados)
        faturamento_hoje = Pedido.objects.filter(
            criado_em__date=timezone.now().date()
        ).exclude(status='cancelado').aggregate(total=Sum('total'))['total'] or 0
        
        context.update({
            'total_produtos': Produto.objects.count(),
            'total_clientes': Cliente.objects.count(),
            'total_pedidos': Pedido.objects.count(),
            'pedidos_hoje': pedidos_hoje_count,
            'faturamento_hoje': faturamento_hoje,
        })
        
        # Pedidos recentes (últimos 5)
        pedidos_recentes = Pedido.objects.select_related('cliente').order_by('-criado_em')[:5]
        context['pedidos_recentes'] = pedidos_recentes
        
        # Dados para gráficos
        context.update({
            'vendas_data': get_vendas_chart_data(),
            'produtos_data': get_produtos_chart_data(),
            'clientes_data': get_clientes_chart_data(),
            'receita_data': get_receita_chart_data(),
        })
    
    return render(request, 'home.html', context)

def get_vendas_chart_data():
    """Dados para gráfico de vendas dos últimos 7 dias"""
    today = timezone.now().date()
    dates = [(today - timedelta(days=i)) for i in range(6, -1, -1)]
    
    data = []
    for date in dates:
        count = Pedido.objects.filter(criado_em__date=date).count()
        data.append({
            'date': date.strftime('%d/%m'),
            'vendas': count
        })
    
    return json.dumps(data)

def get_produtos_chart_data():
    """Dados para gráfico de produtos mais vendidos"""
    # Como ainda não temos itens de pedido, vamos simular dados
    produtos_mock = [
        {'nome': 'Pizza Margherita', 'vendas': 45},
        {'nome': 'Pizza Calabresa', 'vendas': 38},
        {'nome': 'Pizza Portuguesa', 'vendas': 32},
        {'nome': 'Pizza 4 Queijos', 'vendas': 28},
        {'nome': 'Pizza Frango', 'vendas': 25},
    ]
    
    return json.dumps(produtos_mock)

def get_clientes_chart_data():
    """Dados para gráfico de crescimento de clientes"""
    today = timezone.now().date()
    dates = [(today - timedelta(days=i*30)) for i in range(5, -1, -1)]
    
    data = []
    total = 0
    for i, date in enumerate(dates):
        # Simular crescimento
        novos = [12, 18, 25, 32, 28, 35][i]
        total += novos
        data.append({
            'mes': date.strftime('%b'),
            'total': total
        })
    
    return json.dumps(data)

def get_receita_chart_data():
    """Dados para gráfico de receita mensal"""
    receita_mock = [
        {'mes': 'Jan', 'receita': 12500},
        {'mes': 'Fev', 'receita': 15800},
        {'mes': 'Mar', 'receita': 18200},
        {'mes': 'Abr', 'receita': 16900},
        {'mes': 'Mai', 'receita': 21300},
        {'mes': 'Jun', 'receita': 24700},
    ]
    
    return json.dumps(receita_mock)

@login_required
def dashboard_data_api(request):
    """API para atualizar dados do dashboard via AJAX"""
    
    # Calcular faturamento hoje
    faturamento_hoje = Pedido.objects.filter(
        criado_em__date=timezone.now().date(),
        status__in=['confirmado', 'entregue', 'finalizado']
    ).aggregate(total=Sum('total'))['total'] or 0
    
    # Pedidos recentes
    pedidos_recentes = Pedido.objects.select_related('cliente').order_by('-criado_em')[:5]
    pedidos_data = []
    for pedido in pedidos_recentes:
        pedidos_data.append({
            'id': pedido.id,
            'numero': pedido.numero,
            'cliente_nome': pedido.cliente.nome if pedido.cliente else 'Cliente não informado',
            'tipo': pedido.get_tipo_display(),
            'status': pedido.get_status_display(),
            'total': float(pedido.total),
            'criado_em': pedido.criado_em.strftime('%d/%m/%Y %H:%M'),
        })
    
    data = {
        'vendas': json.loads(get_vendas_chart_data()),
        'produtos': json.loads(get_produtos_chart_data()),
        'clientes': json.loads(get_clientes_chart_data()),
        'receita': json.loads(get_receita_chart_data()),
        'stats': {
            'total_produtos': Produto.objects.count(),
            'total_clientes': Cliente.objects.count(),
            'total_pedidos': Pedido.objects.count(),
            'pedidos_hoje': Pedido.objects.filter(
                criado_em__date=timezone.now().date()
            ).count(),
            'faturamento_hoje': float(faturamento_hoje),
        },
        'pedidos_recentes': pedidos_data
    }
    
    return JsonResponse(data)

def pizzas_promocionais_view(request):
    """View para página de pizzas promocionais"""
    from apps.produtos.models import Produto
    from decimal import Decimal
    import json
    
    # Buscar pizzas promocionais por categoria
    pizzas_salgadas = Produto.objects.filter(
        categoria__nome='Pizzas Salgadas',
        ativo=True
    ).order_by('nome')
    
    pizzas_doces = Produto.objects.filter(
        categoria__nome='Pizzas Doces',
        ativo=True
    ).order_by('nome')
    
    bordas = Produto.objects.filter(
        categoria__nome='Bordas Recheadas',
        ativo=True
    ).order_by('preco_unitario')
    
    # Adicionar preço promocional fixo para pizzas que não têm preco_unitario
    preco_promocional = Decimal('40.00')
    
    # Processar pizzas salgadas
    for pizza in pizzas_salgadas:
        if not pizza.preco_unitario:
            pizza.preco_unitario = preco_promocional
            # Tentar obter preços dos tamanhos se existir
            if pizza.tamanhos_precos:
                try:
                    tamanhos_data = json.loads(pizza.tamanhos_precos) if isinstance(pizza.tamanhos_precos, str) else pizza.tamanhos_precos
                    pizza.precos_disponiveis = tamanhos_data
                except:
                    pizza.precos_disponiveis = {}
            else:
                pizza.precos_disponiveis = {}
    
    # Processar pizzas doces
    for pizza in pizzas_doces:
        if not pizza.preco_unitario:
            pizza.preco_unitario = preco_promocional
            # Tentar obter preços dos tamanhos se existir
            if pizza.tamanhos_precos:
                try:
                    tamanhos_data = json.loads(pizza.tamanhos_precos) if isinstance(pizza.tamanhos_precos, str) else pizza.tamanhos_precos
                    pizza.precos_disponiveis = tamanhos_data
                except:
                    pizza.precos_disponiveis = {}
            else:
                pizza.precos_disponiveis = {}
    
    # Calcular total de pizzas
    total_pizzas = pizzas_salgadas.count() + pizzas_doces.count()
    
    context = {
        'pizzas_salgadas': pizzas_salgadas,
        'pizzas_doces': pizzas_doces,
        'bordas': bordas,
        'total_pizzas': total_pizzas,
        'preco_promocional': preco_promocional,
    }
    
    return render(request, 'produtos/pizzas_promocionais.html', context)

def force_login_view(request):
    """View para forçar login de teste"""
    from django.contrib.auth.models import User
    from django.contrib.auth import login as django_login
    
    # Tenta pegar usuário de teste primeiro, depois outros
    user = User.objects.filter(username='test@test.com').first()
    if not user:
        user = User.objects.filter(id=2).first()
    
    if user:
        # Usar backend padrão para usuário com senha
        if user.has_usable_password():
            django_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        else:
            django_login(request, user, backend='authentication.backends.SupabaseBackend')
            
        print(f"FORCE LOGIN: Usuário {user.username} logado manualmente")
        print(f"FORCE LOGIN: Session key = {request.session.session_key}")
        print(f"FORCE LOGIN: User ID na sessão = {request.session.get('_auth_user_id')}")
        return redirect('home')
    else:
        return HttpResponse("Usuário não encontrado")

def test_loading_view(request):
    """View para testar o sistema de loading"""
    return render(request, 'test_loading.html')

