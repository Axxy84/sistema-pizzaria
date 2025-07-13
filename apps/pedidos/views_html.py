from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, TemplateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q, Sum, Count
from django.utils import timezone
from datetime import datetime, timedelta
from decimal import Decimal

from .models import Pedido, ItemPedido
from .forms import PedidoForm, ItemPedidoFormSet, StatusUpdateForm
from apps.clientes.models import Cliente, Endereco
from apps.produtos.models import Produto, ProdutoPreco


class PedidoListView(LoginRequiredMixin, ListView):
    """Lista de pedidos com filtros e busca"""
    model = Pedido
    template_name = 'pedidos/pedido_list.html'
    context_object_name = 'pedidos'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filtro por status
        status = self.request.GET.get('status')
        if status and status != 'todos':
            queryset = queryset.filter(status=status)
        
        # Filtro por tipo
        tipo = self.request.GET.get('tipo')
        if tipo:
            queryset = queryset.filter(tipo=tipo)
        
        # Filtro por data
        data = self.request.GET.get('data')
        if data:
            try:
                data_obj = datetime.strptime(data, '%Y-%m-%d').date()
                queryset = queryset.filter(criado_em__date=data_obj)
            except ValueError:
                pass
        
        # Busca
        busca = self.request.GET.get('busca')
        if busca:
            queryset = queryset.filter(
                Q(numero__icontains=busca) |
                Q(cliente__nome__icontains=busca) |
                Q(cliente__telefone__icontains=busca)
            )
        
        return queryset.select_related('cliente', 'usuario').prefetch_related('itens')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Estatísticas do dia
        hoje = timezone.now().date()
        pedidos_hoje = Pedido.objects.filter(criado_em__date=hoje)
        
        context['total_pedidos_hoje'] = pedidos_hoje.count()
        context['total_vendas_hoje'] = pedidos_hoje.aggregate(
            total=Sum('total')
        )['total'] or 0
        context['ticket_medio'] = (
            context['total_vendas_hoje'] / context['total_pedidos_hoje']
            if context['total_pedidos_hoje'] > 0 else 0
        )
        
        # Contadores por status
        context['status_counts'] = Pedido.objects.values('status').annotate(
            count=Count('id')
        ).order_by('status')
        
        # Filtros ativos
        context['filtro_status'] = self.request.GET.get('status', 'todos')
        context['filtro_tipo'] = self.request.GET.get('tipo', '')
        context['filtro_data'] = self.request.GET.get('data', '')
        context['busca'] = self.request.GET.get('busca', '')
        
        return context


class PedidoCreateView(LoginRequiredMixin, CreateView):
    """Criar novo pedido com wizard"""
    model = Pedido
    form_class = PedidoForm
    template_name = 'pedidos/pedido_form_otimizado.html'
    success_url = reverse_lazy('pedido_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['itens_formset'] = ItemPedidoFormSet(self.request.POST)
        else:
            context['itens_formset'] = ItemPedidoFormSet()
        
        # Dados para o formulário
        context['clientes'] = Cliente.objects.filter(ativo=True).order_by('nome')
        context['produtos'] = Produto.objects.filter(ativo=True).prefetch_related(
            'precos', 'categoria'
        ).order_by('categoria', 'nome')
        
        return context
    
    def form_valid(self, form):
        context = self.get_context_data()
        itens_formset = context['itens_formset']
        
        if itens_formset.is_valid():
            # Salvar pedido
            form.instance.usuario = self.request.user
            self.object = form.save()
            
            # Salvar itens
            itens_formset.instance = self.object
            itens_formset.save()
            
            # Recalcular total após salvar todos os itens
            self.object.calcular_total()
            
            messages.success(
                self.request, 
                f'Pedido #{self.object.numero} criado com sucesso!'
            )
            return redirect(self.success_url)
        else:
            return self.form_invalid(form)


class PedidoDetailView(LoginRequiredMixin, DetailView):
    """Detalhes do pedido com timeline"""
    model = Pedido
    template_name = 'pedidos/pedido_detail.html'
    context_object_name = 'pedido'
    
    def get_queryset(self):
        return super().get_queryset().select_related(
            'cliente', 'usuario', 'endereco_entrega'
        ).prefetch_related('itens__produto_preco__produto')


class PedidoUpdateView(LoginRequiredMixin, UpdateView):
    """Editar pedido existente"""
    model = Pedido
    form_class = PedidoForm
    template_name = 'pedidos/pedido_form.html'
    success_url = reverse_lazy('pedido_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['itens_formset'] = ItemPedidoFormSet(
                self.request.POST, 
                instance=self.object
            )
        else:
            context['itens_formset'] = ItemPedidoFormSet(instance=self.object)
        
        context['clientes'] = Cliente.objects.filter(ativo=True).order_by('nome')
        context['produtos'] = Produto.objects.filter(ativo=True).prefetch_related(
            'precos', 'categoria'
        ).order_by('categoria', 'nome')
        
        return context
    
    def form_valid(self, form):
        context = self.get_context_data()
        itens_formset = context['itens_formset']
        
        if itens_formset.is_valid():
            self.object = form.save()
            itens_formset.save()
            
            # Recalcular total após salvar todos os itens
            self.object.calcular_total()
            
            messages.success(
                self.request, 
                f'Pedido #{self.object.numero} atualizado com sucesso!'
            )
            return redirect(self.success_url)
        else:
            return self.form_invalid(form)



@login_required
def pedido_atualizar_status(request, pk):
    """Atualizar status do pedido com validação"""
    pedido = get_object_or_404(Pedido, pk=pk)
    
    if request.method == 'POST':
        novo_status = request.POST.get('status')
        observacao = request.POST.get('observacao', '')
        forma_pagamento = request.POST.get('forma_pagamento')
        
        # Definir transições válidas para novos status
        # Regras mais flexíveis para operação prática da pizzaria
        transicoes_validas = {
            'recebido': ['preparando', 'entregue', 'cancelado'],  # Permite entrega direta (bebidas, produtos prontos)
            'preparando': ['recebido', 'saindo', 'entregue', 'cancelado'],  # Permite entrega direta (balcão)
            'saindo': ['preparando', 'entregue', 'cancelado'],
            'entregue': ['cancelado'],  # Permite cancelar pedido entregue (estorno)
            'cancelado': []
        }
        
        # Verificar se a transição é válida
        if novo_status in transicoes_validas.get(pedido.status, []):
            # Atualizar status
            pedido.status = novo_status
            
            # Se entregue, atualizar forma de pagamento se fornecida
            if novo_status == 'entregue' and forma_pagamento:
                pedido.forma_pagamento = forma_pagamento
            
            pedido.save()
            
            # TODO: Salvar histórico de status se implementado
            # StatusHistorico.objects.create(
            #     pedido=pedido,
            #     status_anterior=pedido.status,
            #     status_novo=novo_status,
            #     usuario=request.user,
            #     observacao=observacao
            # )
            
            # Resposta para requisições AJAX
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': f'Status do pedido #{pedido.numero} atualizado para {pedido.get_status_display()}',
                    'new_status': novo_status,
                    'status_display': pedido.get_status_display()
                })
            
            messages.success(
                request, 
                f'Status do pedido #{pedido.numero} atualizado para {pedido.get_status_display()}'
            )
        else:
            error_msg = f'Transição de status inválida: {pedido.get_status_display()} → {dict(pedido.STATUS_CHOICES).get(novo_status, novo_status)}'
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'message': error_msg
                }, status=400)
            
            messages.error(request, error_msg)
    
    return redirect('pedidos:pedido_detail', pk=pk)


@login_required
def pedido_cancelar(request, pk):
    """Cancelar pedido"""
    pedido = get_object_or_404(Pedido, pk=pk)
    
    if pedido.status not in ['entregue', 'cancelado']:
        pedido.status = 'cancelado'
        pedido.save()
        messages.success(request, f'Pedido #{pedido.numero} cancelado')
    else:
        messages.error(request, 'Este pedido não pode ser cancelado')
    
    return redirect('pedido_list')


@login_required
def pedido_imprimir(request, pk):
    """Imprimir cupom do pedido"""
    pedido = get_object_or_404(Pedido, pk=pk)
    return render(request, 'pedidos/pedido_print.html', {'pedido': pedido})


# Views AJAX
@login_required
def ajax_buscar_cliente(request):
    """Buscar cliente por nome ou telefone"""
    termo = request.GET.get('termo', '')
    
    if len(termo) >= 3:
        clientes = Cliente.objects.filter(
            Q(nome__icontains=termo) | Q(telefone__icontains=termo),
            ativo=True
        )[:10]
        
        data = []
        for cliente in clientes:
            data.append({
                'id': cliente.id,
                'nome': cliente.nome,
                'telefone': cliente.telefone,
                'email': cliente.email,
                'enderecos': [
                    {
                        'id': e.id,
                        'tipo': e.tipo,
                        'completo': str(e)
                    } for e in cliente.enderecos.all()
                ]
            })
        
        return JsonResponse({'clientes': data})
    
    return JsonResponse({'clientes': []})


@login_required
def ajax_buscar_produtos(request):
    """Buscar produtos para adicionar ao pedido"""
    termo = request.GET.get('termo', '')
    categoria = request.GET.get('categoria', '')
    
    produtos = Produto.objects.filter(ativo=True)
    
    if termo:
        produtos = produtos.filter(nome__icontains=termo)
    
    if categoria:
        produtos = produtos.filter(categoria__id=categoria)
    
    produtos = produtos.prefetch_related('precos')[:20]
    
    data = []
    for produto in produtos:
        precos = []
        for preco in produto.precos.all():
            precos.append({
                'id': preco.id,
                'tamanho': preco.tamanho.nome if preco.tamanho else 'Único',
                'preco': float(preco.preco),
                'preco_promocional': float(preco.preco_promocional) if preco.preco_promocional else None
            })
        
        data.append({
            'id': produto.id,
            'nome': produto.nome,
            'descricao': produto.descricao,
            'categoria': produto.categoria.nome if produto.categoria else '',
            'imagem': produto.imagem.url if produto.imagem else '',
            'precos': precos
        })
    
    return JsonResponse({'produtos': data})


@login_required
def ajax_calcular_taxa_entrega(request):
    """Calcular taxa de entrega baseado no endereço"""
    endereco_id = request.GET.get('endereco_id')
    
    if endereco_id:
        endereco = get_object_or_404(Endereco, id=endereco_id)
        
        # Lógica simplificada de cálculo de taxa
        # Pode ser melhorada com integração de APIs de CEP/distância
        taxa = Decimal('5.00')  # Taxa padrão
        
        # Exemplo: aumentar taxa por bairro
        bairros_distantes = ['Centro', 'Zona Sul', 'Zona Norte']
        if any(b in endereco.bairro for b in bairros_distantes):
            taxa = Decimal('10.00')
        
        return JsonResponse({'taxa_entrega': float(taxa)})
    
    return JsonResponse({'taxa_entrega': 0})


@login_required
def ajax_cliente_enderecos(request, cliente_id):
    """Retornar endereços de um cliente"""
    cliente = get_object_or_404(Cliente, id=cliente_id)
    
    enderecos = []
    for endereco in cliente.enderecos.all():
        enderecos.append({
            'id': endereco.id,
            'tipo': endereco.tipo,
            'completo': str(endereco),
            'principal': endereco.principal
        })
    
    return JsonResponse({'enderecos': enderecos})