from rest_framework import viewsets, status, filters
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from apps.core.cache_utils import CachedViewSetMixin, cache_result, CacheManager
from .models import Pedido, ItemPedido, Mesa
from .models_mesa import Mesa as MesaModel
from .serializers import (
    PedidoListSerializer, PedidoDetailSerializer,
    PedidoCreateSerializer
)
from .utils import SupabaseHealthCheck, PedidoSupabaseManager
from apps.produtos.models import Produto, ProdutoPreco, Tamanho

class PedidoViewSet(CachedViewSetMixin, viewsets.ModelViewSet):
    queryset = Pedido.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['tipo', 'cliente', 'forma_pagamento']
    search_fields = ['numero', 'cliente__nome', 'cliente__telefone']
    ordering_fields = ['criado_em', 'total']
    ordering = ['-criado_em']
    # Cache por 2 minutos para pedidos (mudam frequentemente)
    cache_timeout = 120
    cache_type = 'pedidos'
    
    def get_serializer_class(self):
        if self.action == 'list':
            return PedidoListSerializer
        elif self.action == 'create':
            return PedidoCreateSerializer
        elif self.action == 'atualizar_status':
            return PedidoStatusSerializer
        return PedidoDetailSerializer
    
    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)
    
    # Método atualizar_status removido - use as views específicas
    
    # Método status removido - use as views específicas
    
    @action(detail=False, methods=['get'])
    def pendentes(self, request):
        # Pedidos recém criados (sem preparação iniciada)
        pendentes = self.queryset.filter(
            preparacao_iniciada_em__isnull=True
        ).exclude(status='cancelado')
        serializer = PedidoListSerializer(pendentes, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def em_preparacao(self, request):
        # Pedidos com preparação iniciada mas não finalizados
        em_prep = self.queryset.filter(
            preparacao_iniciada_em__isnull=False,
            entregue_em__isnull=True
        ).exclude(status='cancelado')
        serializer = PedidoListSerializer(em_prep, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def novos(self, request):
        """Verificar novos pedidos desde um timestamp"""
        from django.utils import timezone
        from datetime import datetime
        from django.db.models import Count, Sum
        
        # Pegar timestamp da query string
        desde = request.GET.get('desde')
        
        try:
            if desde:
                # Converter ISO string para datetime, tratando diferentes formatos
                # Remove microsegundos e timezone info para simplificar
                desde_clean = desde.split('.')[0]  # Remove microsegundos
                desde_clean = desde_clean.replace('Z', '')  # Remove Z
                desde_clean = desde_clean.replace('+00:00', '')  # Remove timezone
                
                try:
                    # Tenta parse sem timezone
                    desde_dt = datetime.fromisoformat(desde_clean)
                    # Adiciona timezone UTC
                    desde_dt = timezone.make_aware(desde_dt, timezone.utc)
                except:
                    # Se falhar, tenta com replace direto
                    desde_dt = datetime.fromisoformat(desde.replace('Z', '+00:00').split('.')[0] + '+00:00')
            else:
                # Se não fornecer, usar últimos 5 minutos
                desde_dt = timezone.now() - timezone.timedelta(minutes=5)
            
            # Garantir que está timezone-aware
            if timezone.is_naive(desde_dt):
                desde_dt = timezone.make_aware(desde_dt)
            
            # Buscar novos pedidos
            novos_pedidos = self.queryset.filter(criado_em__gt=desde_dt)
            novos_count = novos_pedidos.count()
            
            # Estatísticas atualizadas
            hoje = timezone.now().date()
            pedidos_hoje = Pedido.objects.filter(criado_em__date=hoje)
            
            total_hoje = pedidos_hoje.count()
            vendas_hoje = pedidos_hoje.aggregate(total=Sum('total'))['total'] or 0
            
            # Contadores por tipo (apenas ativos)
            # Pedidos ativos (não entregues e não cancelados)
            pedidos_ativos = Pedido.objects.filter(
                entregue_em__isnull=True
            ).exclude(status='cancelado')
            pedidos_mesa_count = pedidos_ativos.filter(tipo='mesa').count()
            pedidos_delivery_count = pedidos_ativos.filter(tipo='delivery').count()
            
            return Response({
                'novos_pedidos': novos_count,
                'timestamp': timezone.now().isoformat(),
                'total_hoje': total_hoje,
                'vendas_hoje': float(vendas_hoje),
                'pedidos_mesa_count': pedidos_mesa_count,
                'pedidos_delivery_count': pedidos_delivery_count,
                'pedidos': PedidoListSerializer(novos_pedidos[:10], many=True).data if novos_count > 0 else []
            })
            
        except Exception as e:
            return Response({
                'error': f'Erro ao verificar novos pedidos: {str(e)}'
            }, status=status.HTTP_400_BAD_REQUEST)
    
    
    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def supabase_health(self, request):
        """Endpoint para verificar saúde da integração com Supabase"""
        try:
            status_info = SupabaseHealthCheck.status_completo()
            
            # Determinar status HTTP baseado na conectividade
            http_status = status.HTTP_200_OK if status_info['conectividade'] else status.HTTP_503_SERVICE_UNAVAILABLE
            
            return Response({
                'status': 'ok' if status_info['conectividade'] else 'error',
                'supabase': status_info,
                'timestamp': request.build_absolute_uri().split('?')[0],
                'message': 'Integração funcionando' if status_info['conectividade'] else 'Problemas na integração'
            }, status=http_status)
            
        except Exception as e:
            return Response({
                'status': 'error',
                'message': f'Erro ao verificar status: {str(e)}',
                'timestamp': request.build_absolute_uri().split('?')[0]
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def criar_pedido_seguro(self, request):
        """Endpoint para criar pedido com validações avançadas"""
        try:
            manager = PedidoSupabaseManager()
            dados = request.data if hasattr(request, 'data') else request.POST.dict()
            resultado, erros = manager.criar_pedido_seguro(dados)
            
            if erros:
                return Response({
                    'status': 'error',
                    'erros': erros,
                    'message': 'Falha na validação dos dados'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            return Response({
                'status': 'success',
                'pedido': {
                    'id': resultado['pedido'].id,
                    'numero': resultado['pedido'].numero,
                    'total': float(resultado['total']),
                    'itens_count': len(resultado['itens'])
                },
                'message': 'Pedido criado com sucesso'
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({
                'status': 'error',
                'message': f'Erro interno: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([AllowAny])
def sabores_disponiveis(request):
    """
    Endpoint para listar sabores de pizza disponíveis para meio a meio
    """
    try:
        # Buscar apenas produtos do tipo pizza que tenham preços configurados
        pizzas = Produto.objects.filter(
            tipo_produto='pizza',
            ativo=True,
            precos__isnull=False
        ).distinct().values('id', 'nome', 'descricao')
        
        return Response({
            'status': 'success',
            'sabores': list(pizzas),
            'total': len(pizzas)
        })
    except Exception as e:
        return Response({
            'status': 'error',
            'message': f'Erro ao buscar sabores: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([AllowAny])
def calcular_preco_meio_a_meio(request):
    """
    Endpoint para calcular o preço de uma pizza meio a meio
    """
    try:
        sabor_1_id = request.data.get('sabor_1_id')
        sabor_2_id = request.data.get('sabor_2_id')
        tamanho_id = request.data.get('tamanho_id')
        regra_preco = request.data.get('regra_preco', 'mais_caro')
        
        # Validações
        if not all([sabor_1_id, sabor_2_id, tamanho_id]):
            return Response({
                'status': 'error',
                'message': 'sabor_1_id, sabor_2_id e tamanho_id são obrigatórios'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if sabor_1_id == sabor_2_id:
            return Response({
                'status': 'error',
                'message': 'Os sabores devem ser diferentes'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Buscar produtos e tamanho
        try:
            produto_1 = Produto.objects.get(id=sabor_1_id, tipo_produto='pizza')
            produto_2 = Produto.objects.get(id=sabor_2_id, tipo_produto='pizza')
            tamanho = Tamanho.objects.get(id=tamanho_id)
        except Produto.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'Um dos sabores não foi encontrado ou não é uma pizza'
            }, status=status.HTTP_404_NOT_FOUND)
        except Tamanho.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'Tamanho não encontrado'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Buscar preços
        try:
            preco_1 = ProdutoPreco.objects.get(produto=produto_1, tamanho=tamanho)
            preco_2 = ProdutoPreco.objects.get(produto=produto_2, tamanho=tamanho)
        except ProdutoPreco.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'Preço não encontrado para um dos sabores no tamanho selecionado'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Calcular preço baseado na regra
        if regra_preco == 'mais_caro':
            preco_final = max(preco_1.preco_final, preco_2.preco_final)
        elif regra_preco == 'media':
            preco_final = (preco_1.preco_final + preco_2.preco_final) / 2
        else:
            preco_final = max(preco_1.preco_final, preco_2.preco_final)  # Default para mais caro
        
        return Response({
            'status': 'success',
            'dados': {
                'sabor_1': {
                    'id': produto_1.id,
                    'nome': produto_1.nome,
                    'preco': float(preco_1.preco_final)
                },
                'sabor_2': {
                    'id': produto_2.id,
                    'nome': produto_2.nome,
                    'preco': float(preco_2.preco_final)
                },
                'tamanho': {
                    'id': tamanho.id,
                    'nome': tamanho.nome
                },
                'regra_preco': regra_preco,
                'preco_final': float(preco_final),
                'economia': float(max(preco_1.preco_final, preco_2.preco_final) - preco_final) if regra_preco == 'media' else 0
            }
        })
        
    except Exception as e:
        return Response({
            'status': 'error',
            'message': f'Erro ao calcular preço: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([AllowAny])
def criar_item_meio_a_meio(request):
    """
    Endpoint para criar um item de pedido meio a meio
    """
    try:
        pedido_id = request.data.get('pedido_id')
        sabor_1_id = request.data.get('sabor_1_id')
        sabor_2_id = request.data.get('sabor_2_id')
        tamanho_id = request.data.get('tamanho_id')
        quantidade = int(request.data.get('quantidade', 1))
        regra_preco = request.data.get('regra_preco', 'mais_caro')
        observacoes = request.data.get('observacoes', '')
        
        # Validações
        if not all([pedido_id, sabor_1_id, sabor_2_id, tamanho_id]):
            return Response({
                'status': 'error',
                'message': 'pedido_id, sabor_1_id, sabor_2_id e tamanho_id são obrigatórios'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Buscar objetos
        try:
            pedido = Pedido.objects.get(id=pedido_id)
            produto_1 = Produto.objects.get(id=sabor_1_id, tipo_produto='pizza')
            produto_2 = Produto.objects.get(id=sabor_2_id, tipo_produto='pizza')
            tamanho = Tamanho.objects.get(id=tamanho_id)
        except (Pedido.DoesNotExist, Produto.DoesNotExist, Tamanho.DoesNotExist) as e:
            return Response({
                'status': 'error',
                'message': f'Objeto não encontrado: {str(e)}'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Criar item meio a meio
        item = ItemPedido()
        item.pedido = pedido
        item.quantidade = quantidade
        item.observacoes = observacoes
        
        # Configurar meio a meio
        item.configurar_meio_a_meio(produto_1, produto_2, tamanho, regra_preco)
        item.save()
        
        # Recalcular total do pedido
        pedido.calcular_total()
        
        return Response({
            'status': 'success',
            'item': {
                'id': item.id,
                'descricao': item.get_descricao_completa(),
                'quantidade': item.quantidade,
                'preco_unitario': float(item.preco_unitario),
                'subtotal': float(item.subtotal),
                'is_meio_a_meio': item.is_meio_a_meio,
                'meio_a_meio_data': item.meio_a_meio_data
            },
            'pedido_total': float(pedido.total)
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({
            'status': 'error',
            'message': f'Erro ao criar item meio a meio: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def pedido_confirmacao_view(request, pedido_id):
    """View para exibir a página de confirmação do pedido"""
    pedido = get_object_or_404(Pedido, id=pedido_id)
    return render(request, 'pedidos/confirmacao.html', {'pedido': pedido})


def mesas_abertas_view(request):
    """View principal para gerenciar mesas abertas"""
    mesas = Mesa.objects.filter(status='aberta').order_by('numero')
    
    # Estatísticas
    total_mesas_abertas = mesas.count()
    total_consumo = sum(mesa.total_pedidos for mesa in mesas)
    
    context = {
        'mesas': mesas,
        'total_mesas_abertas': total_mesas_abertas,
        'total_consumo': total_consumo,
    }
    
    return render(request, 'pedidos/mesas_abertas.html', context)


@api_view(['POST'])
@permission_classes([AllowAny])
def criar_pedido_promocional(request):
    """
    API endpoint para processar pedidos promocionais com validações completas
    """
    try:
        data = request.data
        
        # Log da requisição para debug (apenas quando houver erro)
        import json
        import logging
        logger = logging.getLogger(__name__)
        
        # Extrair dados do pedido
        tipo = data.get('tipo', 'balcao')
        cliente_data = data.get('cliente', {})
        mesa_data = data.get('mesa', {})
        endereco_data = data.get('endereco', {})
        pagamento_data = data.get('pagamento', {})
        itens = data.get('itens', [])
        observacoes = data.get('observacoes', '')
        
        # Validações básicas
        if not itens:
            logger.error(f"Pedido sem itens. Dados recebidos: {json.dumps(data, indent=2)}")
            return Response({
                'status': 'error',
                'message': 'É necessário adicionar pelo menos um item ao carrinho'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Validar tipo de pedido
        if tipo not in ['balcao', 'mesa', 'delivery']:
            logger.error(f"Tipo de pedido inválido: {tipo}")
            return Response({
                'status': 'error',
                'message': 'Tipo de pedido inválido'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Validar dados específicos por tipo
        if tipo == 'mesa':
            if not mesa_data.get('numero'):
                logger.error(f"Mesa sem número. Mesa data: {mesa_data}")
                return Response({
                    'status': 'error',
                    'message': 'Número da mesa é obrigatório para pedidos no local'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        if tipo == 'delivery':
            endereco_obrigatorios = ['rua', 'numero', 'bairro']
            for campo in endereco_obrigatorios:
                if not endereco_data.get(campo):
                    logger.error(f"Campo {campo} obrigatório faltando. Endereço: {endereco_data}")
                    return Response({
                        'status': 'error',
                        'message': f'Campo {campo} é obrigatório para delivery'
                    }, status=status.HTTP_400_BAD_REQUEST)
        
        # Validar dados do cliente
        if not cliente_data.get('nome'):
            logger.error(f"Nome do cliente faltando. Cliente: {cliente_data}")
            return Response({
                'status': 'error',
                'message': 'Nome do cliente é obrigatório'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if not cliente_data.get('telefone'):
            return Response({
                'status': 'error',
                'message': 'Telefone do cliente é obrigatório'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Validar pagamento
        forma_pagamento = pagamento_data.get('forma', '')
        if not forma_pagamento:
            return Response({
                'status': 'error',
                'message': 'Forma de pagamento é obrigatória'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Usar manager do Supabase para criar pedido seguro
        manager = PedidoSupabaseManager()
        
        # Preparar dados do pedido
        pedido_data = {
            'tipo': tipo,
            'cliente': cliente_data,
            'mesa': mesa_data if tipo == 'mesa' else None,
            'endereco': endereco_data if tipo == 'delivery' else None,
            'pagamento': pagamento_data,
            'itens': itens,
            'observacoes': observacoes
        }
        
        # Criar pedido com transação segura
        resultado = manager.criar_pedido_completo(pedido_data)
        
        if resultado['status'] == 'success':
            return Response({
                'status': 'success',
                'message': 'Pedido criado com sucesso!',
                'pedido_id': resultado['pedido_id'],
                'numero_pedido': resultado.get('numero_pedido'),
                'total': resultado.get('total'),
                'redirect_url': f'/pedidos/confirmacao/{resultado["pedido_id"]}/'
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'status': 'error',
                'message': resultado.get('message', 'Erro ao criar pedido')
            }, status=status.HTTP_400_BAD_REQUEST)
        
    except Exception as e:
        return Response({
            'status': 'error',
            'message': f'Erro interno do servidor: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@require_http_methods(["POST"])
def abrir_mesa_view(request):
    """View para abrir uma nova mesa"""
    numero = request.POST.get('numero')
    responsavel = request.POST.get('responsavel', '')
    
    if not numero:
        messages.error(request, 'Número da mesa é obrigatório!')
        return redirect('pedidos:mesas_abertas')
    
    # Verificar se a mesa já existe
    mesa_existente = Mesa.objects.filter(numero=numero).first()
    
    if mesa_existente:
        if mesa_existente.status == 'aberta':
            messages.warning(request, f'Mesa {numero} já está aberta!')
        else:
            # Reabrir mesa fechada
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
    
    return redirect('pedidos:mesas_abertas')


@require_http_methods(["POST"])
def fechar_mesa_view(request, mesa_id):
    """View para fechar uma mesa"""
    mesa = get_object_or_404(Mesa, id=mesa_id)
    
    if mesa.status != 'aberta':
        messages.warning(request, f'Mesa {mesa.numero} não está aberta!')
        return redirect('pedidos:mesas_abertas')
    
    # Verificar se há pedidos pendentes
    # Verificar pedidos não finalizados
    pedidos_pendentes = mesa.pedidos_ativos.filter(entregue_em__isnull=True).count()
    
    if pedidos_pendentes > 0 and not request.POST.get('forcar_fechamento'):
        messages.warning(
            request, 
            f'Mesa {mesa.numero} possui {pedidos_pendentes} pedido(s) pendente(s). '
            'Marque a opção de forçar fechamento para continuar.'
        )
        return redirect('pedidos:mesas_abertas')
    
    mesa.fechar_mesa()
    messages.success(request, f'Mesa {mesa.numero} fechada com sucesso! Total: R$ {mesa.total_consumido}')
    
    return redirect('pedidos:mesas_abertas')


def mesa_detalhes_view(request, mesa_id):
    """View para exibir detalhes de uma mesa"""
    mesa = get_object_or_404(Mesa, id=mesa_id)
    pedidos = mesa.pedidos_ativos
    
    context = {
        'mesa': mesa,
        'pedidos': pedidos,
        'comanda': mesa.get_comanda_completa()
    }
    
    return render(request, 'pedidos/mesa_detalhes.html', context)


@require_http_methods(["POST"])
def adicionar_pedido_mesa_view(request, mesa_id):
    """View para adicionar um pedido rápido a uma mesa"""
    mesa = get_object_or_404(Mesa, id=mesa_id)
    
    if mesa.status != 'aberta':
        return JsonResponse({'error': 'Mesa não está aberta'}, status=400)
    
    # Redirecionar para o formulário de pedido com a mesa pré-selecionada
    return redirect(f'/pedidos/novo/?mesa={mesa.numero}')


def imprimir_comanda_view(request, mesa_id):
    """View para imprimir a comanda de uma mesa"""
    mesa = get_object_or_404(Mesa, id=mesa_id)
    comanda = mesa.get_comanda_completa()
    
    context = {
        'mesa': mesa,
        'comanda': comanda,
        'imprimir': True
    }
    
    return render(request, 'pedidos/comanda_impressao.html', context)