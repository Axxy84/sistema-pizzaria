from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, DetailView, UpdateView, TemplateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
import json
from django.db.models import Q, Sum, Count
from django.utils import timezone
from datetime import datetime, timedelta
from decimal import Decimal

from .models import Pedido, ItemPedido, ConfiguracaoPedido
from .models_mesa import Mesa
from .forms import PedidoForm, ItemPedidoFormSet
from apps.clientes.models import Cliente, Endereco
from apps.produtos.models import Produto, ProdutoPreco


class PedidoListView(LoginRequiredMixin, ListView):
    """Lista de pedidos com filtros e busca"""
    model = Pedido
    template_name = 'pedidos/pedido_list.html'
    context_object_name = 'pedidos'
    paginate_by = 20
    
    def get(self, request, *args, **kwargs):
        # Não fazer redirecionamento, processar diretamente
        return super().get(request, *args, **kwargs)
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filtro por status - removido pois status agora é calculado
        # Para filtrar por status, precisaríamos filtrar pelos campos de timestamp
        
        # Filtro por tipo - apenas aplica se for uma view específica
        view = self.request.GET.get('view')
        tipo = self.request.GET.get('tipo')
        
        # Se está em uma view específica (mesa/delivery), aplicar filtro automaticamente
        if view == 'mesa':
            queryset = queryset.filter(tipo='mesa')
        elif view == 'delivery':
            queryset = queryset.filter(tipo='delivery')
        elif tipo and view != 'todos':  # Se tem tipo mas não é view todos, aplicar
            queryset = queryset.filter(tipo=tipo)
        # Se não tem view ou é 'todos', mostrar todos os pedidos
        
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
        
        return queryset.select_related('cliente', 'usuario').prefetch_related('itens').order_by('-criado_em')
    
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
        
        # Contadores por status calculado
        todos_pedidos = Pedido.objects.all()
        status_counts = {}
        for pedido in todos_pedidos:
            status = pedido.status
            if status not in status_counts:
                status_counts[status] = 0
            status_counts[status] += 1
        
        context['status_counts'] = [
            {'status': status, 'count': count} 
            for status, count in status_counts.items()
        ]
        
        # Contadores por tipo para as abas (pedidos não finalizados)
        pedidos_ativos = Pedido.objects.filter(
            entregue_em__isnull=True,
        )
        context['pedidos_mesa_count'] = pedidos_ativos.filter(tipo='mesa').count()
        context['pedidos_delivery_count'] = pedidos_ativos.filter(tipo='delivery').count()
        
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
    template_name = 'pedidos/pedido_rapido.html'
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
    template_name = 'pedidos/pedido_rapido.html'
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
        
        # Função legada - redirecionar para usar as novas funções
        messages.warning(
            request,
            'Use os botões de ação específicos para atualizar o status do pedido.'
        )
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'message': 'Use as APIs específicas: iniciar-preparo, confirmar-saida, confirmar-entrega ou cancelar-com-senha'
            }, status=400)
    
    # Só redireciona se não for AJAX
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        return redirect('pedidos:pedido_detail', pk=pk)
    
    # Se chegou aqui e é AJAX, retorna erro genérico
    return JsonResponse({
        'success': False,
        'message': 'Erro ao processar requisição'
    }, status=400)


@login_required
def pedido_cancelar(request, pk):
    """Cancelar pedido - redireciona para cancelamento com senha"""
    messages.info(request, 'Use o botão de cancelar com senha para cancelar o pedido.')
    return redirect('pedidos:pedido_detail', pk=pk)


@login_required
def pedido_cancelar_com_senha_ajax(request, pk):
    """Cancelar pedido com verificação de senha via AJAX"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Método não permitido'}, status=405)
    
    pedido = get_object_or_404(Pedido, pk=pk)
    password = request.POST.get('password', '')
    motivo = request.POST.get('motivo', '')
    
    # Verificar se o pedido pode ser cancelado
    if not pedido.pode_cancelar:
        return JsonResponse({
            'success': False,
            'message': 'Este pedido não pode ser cancelado'
        })
    
    # Verificar senha configurada no settings
    from django.conf import settings
    senha_correta = getattr(settings, 'PEDIDO_CANCELAMENTO_SENHA', '1234')
    
    if password == senha_correta:
        pedido.status = 'cancelado'
        pedido.save()
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': f'Pedido #{pedido.numero} cancelado com sucesso'
            })
        
        messages.success(request, f'Pedido #{pedido.numero} cancelado com sucesso')
        return redirect('pedidos:pedido_detail', pk=pk)
    
    # Senha incorreta
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': False,
            'message': 'Senha incorreta!'
        })
    
    messages.error(request, 'Senha incorreta!')
    return redirect('pedidos:pedido_detail', pk=pk)


@login_required
def pedido_iniciar_preparo(request, pk):
    """Inicia o preparo do pedido"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Método não permitido'}, status=405)
    
    pedido = get_object_or_404(Pedido, pk=pk)
    
    if not pedido.pode_iniciar_preparo:
        return JsonResponse({
            'success': False,
            'message': 'Não é possível iniciar o preparo deste pedido'
        })
    
    pedido.preparacao_iniciada_em = timezone.now()
    pedido.save()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'message': f'Preparo do pedido #{pedido.numero} iniciado'
        })
    
    messages.success(request, f'Preparo do pedido #{pedido.numero} iniciado')
    return redirect('pedidos:pedido_detail', pk=pk)


@login_required
def pedido_confirmar_saida(request, pk):
    """Confirma saída do pedido para entrega"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Método não permitido'}, status=405)
    
    pedido = get_object_or_404(Pedido, pk=pk)
    
    if not pedido.pode_confirmar_saida:
        return JsonResponse({
            'success': False,
            'message': 'Não é possível confirmar saída deste pedido'
        })
    
    pedido.saida_confirmada_em = timezone.now()
    pedido.save()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'message': f'Saída do pedido #{pedido.numero} confirmada'
        })
    
    messages.success(request, f'Saída do pedido #{pedido.numero} confirmada')
    return redirect('pedidos:pedido_detail', pk=pk)


@login_required
def pedido_confirmar_entrega(request, pk):
    """Confirma entrega do pedido"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Método não permitido'}, status=405)
    
    pedido = get_object_or_404(Pedido, pk=pk)
    
    if not pedido.pode_confirmar_entrega:
        return JsonResponse({
            'success': False,
            'message': 'Não é possível confirmar entrega deste pedido'
        })
    
    pedido.entregue_em = timezone.now()
    pedido.save()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'message': f'Pedido #{pedido.numero} entregue com sucesso'
        })
    
    messages.success(request, f'Pedido #{pedido.numero} entregue com sucesso')
    return redirect('pedidos:pedido_detail', pk=pk)


@login_required
def pedido_imprimir(request, pk):
    """Imprimir cupom do pedido"""
    pedido = get_object_or_404(Pedido, pk=pk)
    return render(request, 'pedidos/pedido_print.html', {'pedido': pedido})


@login_required
def pedido_comanda_cozinha(request, pk):
    """Imprimir comanda simplificada para cozinha"""
    pedido = get_object_or_404(Pedido, pk=pk)
    return render(request, 'pedidos/comanda_cozinha.html', {'pedido': pedido})


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


class PedidoRapidoView(LoginRequiredMixin, TemplateView):
    """View para novo sistema de pedido rápido unificado"""
    template_name = 'pedidos/pedido_rapido.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


def api_criar_pedido_rapido(request):
    """API para criar pedido do sistema rápido"""
    import traceback
    
    # Wrapper completo para capturar QUALQUER erro
    try:
        print(f"DEBUG: =====INÍCIO api_criar_pedido_rapido=====")
        print(f"DEBUG: request = {request}")
        print(f"DEBUG: type(request) = {type(request)}")
        
        # Verificar se request não é None
        if request is None:
            print(f"ERRO: request é None!")
            return JsonResponse({'error': 'Request é None'}, status=500)
        
        # Verificar autenticação manualmente
        if hasattr(request, 'user'):
            print(f"DEBUG: request.user = {request.user}")
            print(f"DEBUG: user.is_authenticated = {request.user.is_authenticated if request.user else 'user é None'}")
        else:
            print(f"DEBUG: request NÃO tem atributo 'user'")
        
        # Verificar método
        if hasattr(request, 'method'):
            print(f"DEBUG: request.method = {request.method}")
            if request.method != 'POST':
                return JsonResponse({'error': 'Método não permitido'}, status=405)
        else:
            print(f"ERRO: request não tem atributo 'method'!")
            return JsonResponse({'error': 'Request inválido - sem method'}, status=500)
    
    except Exception as e:
        print(f"ERRO CRÍTICO CAPTURADO NO WRAPPER: {str(e)}")
        print(f"Tipo do erro: {type(e)}")
        print(f"Traceback:\n{traceback.format_exc()}")
        return JsonResponse({
            'error': f'Erro crítico: {str(e)}',
            'traceback': traceback.format_exc()
        }, status=500)
    
    try:
        # Debug completo do request
        print(f"DEBUG: Verificando atributos do request...")
        print(f"DEBUG: request = {request}")
        print(f"DEBUG: type(request) = {type(request)}")
        
        # Verificar se request tem os atributos esperados
        if hasattr(request, 'body'):
            print(f"DEBUG: request.body = {request.body}")
        else:
            print(f"DEBUG: request NÃO tem atributo 'body'")
            
        if hasattr(request, 'POST'):
            print(f"DEBUG: request.POST = {request.POST}")
        else:
            print(f"DEBUG: request NÃO tem atributo 'POST'")
            
        if hasattr(request, 'content_type'):
            print(f"DEBUG: request.content_type = {request.content_type}")
        else:
            print(f"DEBUG: request NÃO tem atributo 'content_type'")
        
        # Verificar se o body está vazio
        if not request.body:
            return JsonResponse({
                'error': 'Corpo da requisição vazio'
            }, status=400)
        
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError as e:
            print(f"DEBUG: Erro ao decodificar JSON: {e}")
            return JsonResponse({
                'error': f'JSON inválido: {str(e)}'
            }, status=400)
        
        print(f"DEBUG: Dados recebidos: {json.dumps(data, indent=2) if data else 'None'}")
        
        # Validar dados obrigatórios
        if not data or not isinstance(data, dict):
            return JsonResponse({
                'error': 'Dados inválidos'
            }, status=400)
            
        if not data.get('itens'):
            return JsonResponse({
                'error': 'Pedido deve conter pelo menos um item'
            }, status=400)
        
        # Criar ou buscar cliente
        cliente = None
        if data and isinstance(data, dict) and data.get('cliente_nome'):
            # Buscar por telefone se fornecido
            if data.get('cliente_telefone'):
                cliente = Cliente.objects.filter(
                    telefone=data['cliente_telefone']
                ).first()
            
            # Se não encontrar, criar novo
            if not cliente:
                try:
                    cliente = Cliente.objects.create(
                        nome=data['cliente_nome'],
                        telefone=data.get('cliente_telefone', ''),
                        email=data.get('cliente_email', '')
                    )
                except Exception as e:
                    raise
                
                # Criar endereço se for delivery
                if data.get('tipo') == 'delivery' and data.get('endereco_entrega'):
                    try:
                        endereco = Endereco.objects.create(
                            cliente=cliente,
                            tipo='residencial',
                            logradouro=data['endereco_entrega'],
                            principal=True
                        )
                    except Exception as e:
                        raise
        
        # Criar pedido
        
        # Processar forma de pagamento (única ou múltipla)
        if data is None:
            print(f"ERRO: data é None ao processar forma de pagamento!")
            return JsonResponse({'error': 'Dados inválidos'}, status=400)
            
        forma_pagamento = data.get('forma_pagamento', 'dinheiro') if data else 'dinheiro'
        formas_pagamento_multiplas = data.get('formas_pagamento', []) if data else []
        
        # Se tiver múltiplas formas, usar a primeira como principal
        if formas_pagamento_multiplas and len(formas_pagamento_multiplas) > 0:
            primeiro_pagamento = formas_pagamento_multiplas[0]
            if isinstance(primeiro_pagamento, dict):
                forma_pagamento = primeiro_pagamento.get('tipo', 'dinheiro')
            else:
                forma_pagamento = 'dinheiro'
        
        try:
            # Preparar dados do pedido com verificações defensivas
            tipo_pedido = data.get('tipo', 'balcao') if data else 'balcao'
            mesa = ''
            if data and data.get('tipo') == 'mesa':
                mesa = data.get('mesa', '')
            
            taxa_entrega_str = '0'
            if data and data.get('taxa_entrega') is not None:
                taxa_entrega_str = str(data.get('taxa_entrega', 0))
            
            observacoes = ''
            if data and data.get('observacoes'):
                observacoes = data.get('observacoes', '')
            
            pedido = Pedido.objects.create(
                cliente=cliente,
                usuario=request.user,
                tipo=tipo_pedido,
                mesa=mesa,
                mesa_numero=mesa,  # Usar o novo campo mesa_numero também
                forma_pagamento=forma_pagamento,
                taxa_entrega=Decimal(taxa_entrega_str),
                observacoes=observacoes
            )
            
            # Se for pedido de mesa, criar ou atualizar a mesa
            if tipo_pedido == 'mesa' and mesa:
                mesa_obj, created = Mesa.objects.get_or_create(
                    numero=mesa,
                    defaults={
                        'status': 'aberta',
                        'aberta_em': timezone.now()
                    }
                )
                
                # Se a mesa já existia mas estava fechada, reabrir
                if not created and mesa_obj.status == 'fechada':
                    mesa_obj.reabrir_mesa()
            
            # TODO: Salvar formas de pagamento múltiplas em tabela separada se necessário
        except Exception as e:
            raise
        
        # Adicionar itens
        itens_adicionados = 0
        itens_list = data.get('itens', []) if data else []
        
        print(f"DEBUG: Total de itens a processar: {len(itens_list)}")
        print(f"DEBUG: Tipo de itens_list: {type(itens_list)}")
        
        # Verificar se itens_list é uma lista
        if not isinstance(itens_list, list):
            print(f"ERRO: itens não é uma lista: {type(itens_list)}")
            return JsonResponse({'error': 'Formato de itens inválido'}, status=400)
        
        for idx, item_data in enumerate(itens_list):
            print(f"DEBUG: Processando item {idx}: {item_data}")
            print(f"DEBUG: Tipo do item: {type(item_data)}")
            
            if item_data is None:
                print(f"DEBUG: Item {idx} é None, pulando")
                continue
                
            if not isinstance(item_data, dict):
                print(f"DEBUG: Item {idx} não é um dicionário: {type(item_data)}, pulando")
                continue
                
            observacao = item_data.get('observacoes', '')
            
            # Buscar produto_preco
            produto_preco = None
            produto_preco_id = item_data.get('produto_preco_id')
            print(f"DEBUG: produto_preco_id = {produto_preco_id}")
            
            if produto_preco_id:
                try:
                    produto_preco = ProdutoPreco.objects.filter(
                        id=produto_preco_id
                    ).first()
                    print(f"DEBUG: produto_preco encontrado: {produto_preco}")
                except Exception as e:
                    print(f"DEBUG: Erro ao buscar produto_preco: {type(e).__name__}: {str(e)}")
                    pass  # Ignorar erro e continuar
            else:
                print(f"DEBUG: produto_preco_id é None ou vazio para item {idx}")
            
            if produto_preco:
                try:
                    quantidade = int(item_data.get('quantidade', 1))
                    
                    # Criar item (o save automático calculará preco_unitario e subtotal)
                    item_pedido = ItemPedido(
                        pedido=pedido,
                        produto_preco=produto_preco,
                        quantidade=quantidade,
                        observacoes=observacao
                    )
                    
                    # Se for pizza meio a meio, configurar antes de salvar
                    if item_data and isinstance(item_data, dict) and item_data.get('meio_a_meio'):
                        meio_a_meio_data = item_data.get('meio_a_meio_data')
                        if meio_a_meio_data and isinstance(meio_a_meio_data, dict):
                            item_pedido.meio_a_meio_data = meio_a_meio_data
                        else:
                            print(f"DEBUG: Dados meio a meio inválidos: {meio_a_meio_data}")
                    
                    # Salvar (calculará preços automaticamente)
                    item_pedido.save()
                    itens_adicionados += 1
                    
                except Exception as e:
                    raise
        
        # Verificar se adicionou algum item
        if itens_adicionados == 0:
            # Deletar pedido vazio
            pedido.delete()
            return JsonResponse({
                'error': 'Nenhum item válido foi encontrado para adicionar ao pedido'
            }, status=400)
        
        # Calcular total
        try:
            pedido.calcular_total()
        except Exception as e:
            print(f"DEBUG: Erro ao calcular total: {type(e).__name__}: {str(e)}")
            # Se der erro ao calcular, fazer manualmente
            pedido.subtotal = Decimal('0')
            pedido.total = Decimal('0')
            for item in pedido.itens.all():
                pedido.subtotal += item.subtotal
            pedido.total = pedido.subtotal + pedido.taxa_entrega - pedido.desconto
            pedido.save()
        
        return JsonResponse({
            'success': True,
            'pedido_id': pedido.id,
            'numero': pedido.numero,
            'total': float(pedido.total)
        })
        
    except json.JSONDecodeError as e:
        print(f"DEBUG: Erro ao decodificar JSON: {str(e)}")
        return JsonResponse({
            'error': f'JSON inválido: {str(e)}'
        }, status=400)
    except Exception as e:
        print(f"DEBUG: Erro geral: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        return JsonResponse({
            'error': f'Erro ao criar pedido: {str(e)}'
        }, status=400)


# Views para atualização de status de pedidos

@login_required
def pedido_atualizar_status(request, pk):
    """View genérica para atualizar status do pedido"""
    pedido = get_object_or_404(Pedido, pk=pk)
    
    if request.method == 'POST':
        # Capturar o parâmetro status ou action
        status = request.POST.get('status') or request.POST.get('action')
        
        try:
            success_message = ''
            
            if status == 'iniciar_preparo' or status == 'preparando':
                if pedido.preparacao_iniciada_em:
                    success_message = f'Preparação do pedido {pedido.numero} já foi iniciada!'
                else:
                    pedido.preparacao_iniciada_em = timezone.now()
                    pedido.save()
                    success_message = f'Preparação do pedido {pedido.numero} iniciada!'
                
            elif status == 'confirmar_saida' or status == 'saiu_entrega':
                if not pedido.preparacao_iniciada_em:
                    raise ValueError('Preparação deve ser iniciada antes de confirmar saída!')
                elif pedido.saiu_entrega_em:
                    success_message = f'Saída do pedido {pedido.numero} já foi confirmada!'
                else:
                    pedido.saiu_entrega_em = timezone.now()
                    pedido.save()
                    success_message = f'Saída do pedido {pedido.numero} confirmada!'
                
            elif status == 'confirmar_entrega' or status == 'entregue':
                if pedido.tipo == 'delivery' and not pedido.saiu_entrega_em:
                    raise ValueError('Saída deve ser confirmada antes de confirmar entrega!')
                elif pedido.entregue_em:
                    success_message = f'Entrega do pedido {pedido.numero} já foi confirmada!'
                else:
                    pedido.entregue_em = timezone.now()
                    pedido.save()
                    success_message = f'Entrega do pedido {pedido.numero} confirmada!'
                    
            elif status == 'cancelar':
                if pedido.status == 'cancelado':
                    success_message = f'Pedido {pedido.numero} já está cancelado!'
                else:
                    pedido.status = 'cancelado'
                    pedido.save()
                    success_message = f'Pedido {pedido.numero} cancelado!'
                
            else:
                raise ValueError(f'Status inválido: {status}')
            
            # Se for requisição AJAX, retornar JSON
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': success_message,
                    'status': status,
                    'pedido_id': pedido.id
                })
            else:
                messages.success(request, success_message)
                
        except Exception as e:
            error_message = f'Erro ao atualizar status: {str(e)}'
            
            # Se for requisição AJAX, retornar JSON de erro
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'message': error_message
                }, status=400)
            else:
                messages.error(request, error_message)
    
    # Para requisições não-AJAX, redirecionar
    return redirect('pedidos:pedido_detail', pk=pedido.pk)


@login_required
def pedido_cancelar_com_senha(request, pk):
    """View para cancelar pedido com senha de proteção"""
    pedido = get_object_or_404(Pedido, pk=pk)
    
    if request.method == 'POST':
        senha = request.POST.get('senha_cancelamento')
        motivo = request.POST.get('motivo', '')
        
        # Verificar senha usando o modelo de configuração
        config = ConfiguracaoPedido.get_configuracao()
        
        if config.check_senha_cancelamento(senha):
            try:
                pedido.status = 'cancelado'
                pedido.save()
                messages.success(request, f'Pedido {pedido.numero} cancelado com sucesso!')
                return redirect('pedidos:pedido_detail', pk=pedido.pk)
                
            except Exception as e:
                messages.error(request, f'Erro ao cancelar pedido: {str(e)}')
        else:
            messages.error(request, 'Senha incorreta!')
    
    return render(request, 'pedidos/cancelar_com_senha.html', {'pedido': pedido})


@login_required
def pedido_iniciar_preparo(request, pk):
    """View específica para iniciar preparação"""
    pedido = get_object_or_404(Pedido, pk=pk)
    
    if request.method == 'POST':
        try:
            if pedido.preparacao_iniciada_em:
                messages.warning(request, f'Preparação do pedido {pedido.numero} já foi iniciada!')
            else:
                pedido.preparacao_iniciada_em = timezone.now()
                pedido.save()
                messages.success(request, f'Preparação do pedido {pedido.numero} iniciada!')
                
        except Exception as e:
            messages.error(request, f'Erro ao iniciar preparação: {str(e)}')
    
    return redirect('pedidos:pedido_detail', pk=pedido.pk)


@login_required
def pedido_confirmar_saida(request, pk):
    """View específica para confirmar saída para entrega"""
    pedido = get_object_or_404(Pedido, pk=pk)
    
    if request.method == 'POST':
        try:
            if not pedido.preparacao_iniciada_em:
                messages.error(request, 'Preparação deve ser iniciada antes de confirmar saída!')
            elif pedido.saiu_entrega_em:
                messages.warning(request, f'Saída do pedido {pedido.numero} já foi confirmada!')
            else:
                pedido.saiu_entrega_em = timezone.now()
                pedido.save()
                messages.success(request, f'Saída do pedido {pedido.numero} confirmada!')
                
        except Exception as e:
            messages.error(request, f'Erro ao confirmar saída: {str(e)}')
    
    return redirect('pedidos:pedido_detail', pk=pedido.pk)


@login_required
def pedido_confirmar_entrega(request, pk):
    """View específica para confirmar entrega"""
    pedido = get_object_or_404(Pedido, pk=pk)
    
    if request.method == 'POST':
        try:
            if pedido.tipo == 'delivery' and not pedido.saiu_entrega_em:
                messages.error(request, 'Saída deve ser confirmada antes de confirmar entrega!')
            elif pedido.entregue_em:
                messages.warning(request, f'Entrega do pedido {pedido.numero} já foi confirmada!')
            else:
                pedido.entregue_em = timezone.now()
                pedido.save()
                messages.success(request, f'Entrega do pedido {pedido.numero} confirmada!')
                
        except Exception as e:
            messages.error(request, f'Erro ao confirmar entrega: {str(e)}')
    
    return redirect('pedidos:pedido_detail', pk=pedido.pk)


@login_required
def pedido_cancelar(request, pk):
    """View simples para cancelar pedido (sem senha)"""
    pedido = get_object_or_404(Pedido, pk=pk)
    
    if request.method == 'POST':
        motivo = request.POST.get('motivo', 'Cancelado pelo usuário')
        
        try:
            if pedido.status == 'cancelado':
                messages.warning(request, f'Pedido {pedido.numero} já está cancelado!')
            else:
                pedido.status = 'cancelado'
                pedido.save()
                messages.success(request, f'Pedido {pedido.numero} cancelado com sucesso!')
                
        except Exception as e:
            messages.error(request, f'Erro ao cancelar pedido: {str(e)}')
    
    return redirect('pedidos:pedido_detail', pk=pedido.pk)


@login_required
def pedido_imprimir(request, pk):
    """View para imprimir pedido"""
    pedido = get_object_or_404(Pedido, pk=pk)
    
    context = {
        'pedido': pedido,
        'itens': pedido.itens.all(),
        'cliente': pedido.cliente,
        'print_mode': True
    }
    
    return render(request, 'pedidos/pedido_print.html', context)


@login_required
def configuracao_senha_cancelamento(request):
    """View para alterar a senha de cancelamento de pedidos"""
    # Verificar se o usuário é admin
    if not request.user.is_staff:
        messages.error(request, 'Você não tem permissão para acessar esta página.')
        return redirect('pedidos:pedido_list')
    
    config = ConfiguracaoPedido.get_configuracao()
    
    if request.method == 'POST':
        senha_atual = request.POST.get('senha_atual', '')
        senha_nova = request.POST.get('senha_nova', '')
        senha_confirmacao = request.POST.get('senha_confirmacao', '')
        
        # Validações
        if not senha_atual:
            messages.error(request, 'Por favor, informe a senha atual.')
        elif not config.check_senha_cancelamento(senha_atual):
            messages.error(request, 'Senha atual incorreta.')
        elif not senha_nova:
            messages.error(request, 'Por favor, informe a nova senha.')
        elif len(senha_nova) < 4:
            messages.error(request, 'A nova senha deve ter pelo menos 4 caracteres.')
        elif senha_nova != senha_confirmacao:
            messages.error(request, 'As senhas não coincidem.')
        else:
            # Alterar a senha
            config.set_senha_cancelamento(senha_nova)
            messages.success(request, 'Senha de cancelamento alterada com sucesso!')
            return redirect('pedidos:configuracao_senha_cancelamento')
    
    context = {
        'config': config,
        'tempo_maximo': config.tempo_maximo_cancelamento,
        'permitir_cancelamento': config.permitir_cancelamento,
    }
    
    return render(request, 'pedidos/configuracao_senha_cancelamento.html', context)