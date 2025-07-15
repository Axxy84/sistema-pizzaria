from rest_framework import viewsets, status, filters
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from .models import Pedido, ItemPedido
from .serializers import (
    PedidoListSerializer, PedidoDetailSerializer,
    PedidoCreateSerializer, PedidoStatusSerializer
)
from .utils import SupabaseHealthCheck, PedidoSupabaseManager
from apps.produtos.models import Produto, ProdutoPreco, Tamanho

class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'tipo', 'cliente', 'forma_pagamento']
    search_fields = ['numero', 'cliente__nome', 'cliente__telefone']
    ordering_fields = ['criado_em', 'total']
    ordering = ['-criado_em']
    
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
    
    @action(detail=True, methods=['patch'])
    def atualizar_status(self, request, pk=None):
        pedido = self.get_object()
        serializer = PedidoStatusSerializer(pedido, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['patch'], url_path='status')
    def status(self, request, pk=None):
        """Atualizar apenas o status do pedido"""
        pedido = self.get_object()
        new_status = request.data.get('status')
        
        if not new_status:
            return Response({'error': 'Status é obrigatório'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Verificar se o status é válido
        status_choices = [choice[0] for choice in Pedido.STATUS_CHOICES]
        if new_status not in status_choices:
            return Response({'error': 'Status inválido'}, status=status.HTTP_400_BAD_REQUEST)
        
        pedido.status = new_status
        pedido.save()
        
        return Response({'status': pedido.status, 'message': 'Status atualizado com sucesso'})
    
    @action(detail=False, methods=['get'])
    def pendentes(self, request):
        pendentes = self.queryset.filter(status='pendente')
        serializer = PedidoListSerializer(pendentes, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def em_preparacao(self, request):
        em_prep = self.queryset.filter(status__in=['confirmado', 'preparando'])
        serializer = PedidoListSerializer(em_prep, many=True)
        return Response(serializer.data)
    
    
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