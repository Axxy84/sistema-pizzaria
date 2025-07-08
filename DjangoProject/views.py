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
        context.update({
            'total_produtos': Produto.objects.count(),
            'total_clientes': Cliente.objects.count(),
            'total_pedidos': Pedido.objects.count(),
            'pedidos_hoje': Pedido.objects.filter(
                data_pedido__date=timezone.now().date()
            ).count(),
        })
        
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
        count = Pedido.objects.filter(data_pedido__date=date).count()
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
                data_pedido__date=timezone.now().date()
            ).count(),
        }
    }
    
    return JsonResponse(data)

def force_login_view(request):
    """View para forçar login de teste"""
    from django.contrib.auth.models import User
    from django.contrib.auth import login as django_login
    
    # Pega o usuário existente
    user = User.objects.filter(id=2).first()
    if user:
        django_login(request, user, backend='authentication.backends.SupabaseBackend')
        print(f"FORCE LOGIN: Usuário {user.username} logado manualmente")
        return redirect('home')
    else:
        return HttpResponse("Usuário não encontrado")