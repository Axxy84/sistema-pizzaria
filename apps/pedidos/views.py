from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Pedido, ItemPedido
from .serializers import (
    PedidoListSerializer, PedidoDetailSerializer,
    PedidoCreateSerializer, PedidoStatusSerializer
)

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