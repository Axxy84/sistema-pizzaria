from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from .models import Pedido, ItemPedido
from .serializers import (
    PedidoListSerializer, PedidoDetailSerializer,
    PedidoCreateSerializer, PedidoStatusSerializer
)
from .utils import SupabaseHealthCheck, PedidoSupabaseManager

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
            dados = getattr(request, 'data', request.POST.dict())
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