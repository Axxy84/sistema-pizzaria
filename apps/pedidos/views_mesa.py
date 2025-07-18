from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.db import transaction
from django.utils import timezone
from django.template.loader import render_to_string
from decimal import Decimal
import json

from .models_mesa import Mesa
from .models import Pedido, ItemPedido
from apps.produtos.models import ProdutoPreco
from apps.clientes.models import Cliente

@login_required
def listar_mesas(request):
    """Lista todas as mesas abertas"""
    mesas_abertas = Mesa.objects.filter(status='aberta').order_by('numero')
    mesas_fechadas = Mesa.objects.filter(status='fechada').order_by('-fechada_em')[:10]  # Últimas 10 fechadas
    
    context = {
        'mesas_abertas': mesas_abertas,
        'mesas_fechadas': mesas_fechadas,
        'total_mesas_abertas': mesas_abertas.count(),
    }
    
    return render(request, 'pedidos/mesas_abertas.html', context)

@login_required
def abrir_mesa(request):
    """Abre uma nova mesa"""
    if request.method == 'POST':
        numero = request.POST.get('numero')
        responsavel = request.POST.get('responsavel', '')
        
        # Verificar se a mesa já existe
        mesa_existente = Mesa.objects.filter(numero=numero).first()
        
        if mesa_existente:
            if mesa_existente.status == 'aberta':
                messages.error(request, f'Mesa {numero} já está aberta!')
            else:
                # Reabrir mesa
                mesa_existente.reabrir_mesa()
                mesa_existente.responsavel = responsavel
                mesa_existente.save()
                messages.success(request, f'Mesa {numero} reaberta com sucesso!')
        else:
            # Criar nova mesa
            Mesa.objects.create(
                numero=numero,
                responsavel=responsavel,
                status='aberta'
            )
            messages.success(request, f'Mesa {numero} aberta com sucesso!')
        
        return redirect('pedidos:listar_mesas')
    
    return redirect('pedidos:listar_mesas')

@login_required
def detalhes_mesa(request, mesa_id):
    """Exibe detalhes de uma mesa específica"""
    mesa = get_object_or_404(Mesa, id=mesa_id)
    pedidos = mesa.pedidos_ativos
    
    context = {
        'mesa': mesa,
        'pedidos': pedidos,
        'total_mesa': mesa.total_pedidos,
    }
    
    return render(request, 'pedidos/mesa_detalhes.html', context)

@login_required
def adicionar_pedido_mesa(request, mesa_id):
    """Adiciona um novo pedido à mesa"""
    mesa = get_object_or_404(Mesa, id=mesa_id)
    
    if request.method == 'POST':
        try:
            with transaction.atomic():
                # Criar pedido
                pedido = Pedido.objects.create(
                    tipo='mesa',
                    mesa_numero=mesa.numero,
                    usuario=request.user,
                    status='recebido',
                    forma_pagamento='dinheiro',  # Será definido ao fechar a mesa
                    observacoes=request.POST.get('observacoes', '')
                )
                
                # Processar itens do pedido
                itens_json = request.POST.get('itens', '[]')
                itens = json.loads(itens_json)
                
                for item in itens:
                    produto_preco = get_object_or_404(ProdutoPreco, id=item['produto_preco_id'])
                    
                    item_pedido = ItemPedido.objects.create(
                        pedido=pedido,
                        produto_preco=produto_preco,
                        quantidade=item['quantidade'],
                        preco_unitario=produto_preco.preco_final,
                        observacoes=item.get('observacoes', '')
                    )
                    
                    # Se for meio a meio
                    if item.get('meio_a_meio'):
                        item_pedido.meio_a_meio_data = item['meio_a_meio']
                        item_pedido.save()
                
                # Calcular total do pedido
                pedido.calcular_total()
                
                messages.success(request, f'Pedido #{pedido.numero} adicionado à mesa {mesa.numero}!')
                return JsonResponse({'success': True, 'pedido_id': pedido.id})
                
        except Exception as e:
            messages.error(request, f'Erro ao adicionar pedido: {str(e)}')
            return JsonResponse({'success': False, 'error': str(e)})
    
    # GET - Mostrar formulário
    from apps.produtos.models import Produto, Categoria
    
    categorias = Categoria.objects.all()
    produtos = Produto.objects.filter(ativo=True).prefetch_related('precos__tamanho')
    
    context = {
        'mesa': mesa,
        'categorias': categorias,
        'produtos': produtos,
    }
    
    return render(request, 'pedidos/adicionar_pedido_mesa.html', context)

@login_required
def fechar_mesa(request, mesa_id):
    """Fecha uma mesa e permite imprimir comanda"""
    mesa = get_object_or_404(Mesa, id=mesa_id)
    
    if request.method == 'POST':
        forma_pagamento = request.POST.get('forma_pagamento')
        
        # Atualizar forma de pagamento de todos os pedidos
        mesa.pedidos_ativos.update(forma_pagamento=forma_pagamento)
        
        # Fechar mesa
        mesa.fechar_mesa()
        
        messages.success(request, f'Mesa {mesa.numero} fechada com sucesso!')
        
        # Se for requisição AJAX, retornar resposta apropriada
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return HttpResponse(status=200)
        
        # Se solicitado, redirecionar para impressão
        if request.POST.get('imprimir_comanda'):
            return redirect('pedidos:imprimir_comanda_mesa', mesa_id=mesa.id)
        
        return redirect('pedidos:listar_mesas')
    
    # GET - Mostrar resumo para fechamento
    context = {
        'mesa': mesa,
        'pedidos': mesa.pedidos_ativos,
        'total': mesa.total_pedidos,
        'formas_pagamento': Pedido.PAGAMENTO_CHOICES,
    }
    
    return render(request, 'pedidos/fechar_mesa.html', context)

@login_required
def imprimir_comanda_mesa(request, mesa_id):
    """Gera comanda completa da mesa para impressão"""
    mesa = get_object_or_404(Mesa, id=mesa_id)
    
    # Buscar todos os pedidos da mesa (não apenas ativos)
    pedidos = Pedido.objects.filter(
        tipo='mesa',
        mesa_numero=mesa.numero
    ).prefetch_related(
        'itens__produto_preco__produto',
        'itens__produto_preco__tamanho'
    ).order_by('criado_em')
    
    context = {
        'mesa': mesa,
        'pedidos': pedidos,
        'data_impressao': timezone.now(),
        'total': sum(p.total for p in pedidos),
    }
    
    return render(request, 'pedidos/comanda_mesa_impressao.html', context)

@login_required
def api_status_mesa(request, mesa_id):
    """API para obter status atualizado da mesa"""
    mesa = get_object_or_404(Mesa, id=mesa_id)
    
    pedidos_data = []
    for pedido in mesa.pedidos_ativos:
        itens_data = []
        for item in pedido.itens.all():
            itens_data.append({
                'descricao': item.get_descricao_completa(),
                'quantidade': item.quantidade,
                'preco_unitario': float(item.preco_unitario),
                'subtotal': float(item.subtotal),
            })
        
        pedidos_data.append({
            'numero': pedido.numero,
            'status': pedido.get_status_display(),
            'criado_em': pedido.criado_em.strftime('%H:%M'),
            'tempo': pedido.tempo_desde_criacao,
            'itens': itens_data,
            'total': float(pedido.total),
        })
    
    data = {
        'mesa': {
            'numero': mesa.numero,
            'status': mesa.get_status_display(),
            'tempo_aberta': mesa.tempo_aberta,
            'responsavel': mesa.responsavel,
        },
        'pedidos': pedidos_data,
        'total': float(mesa.total_pedidos),
    }
    
    return JsonResponse(data)