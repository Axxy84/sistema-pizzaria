from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db import models
from .models import UnidadeMedida, Ingrediente, MovimentoEstoque, ReceitaProduto
from .serializers import (
    UnidadeMedidaSerializer, IngredienteListSerializer,
    IngredienteDetailSerializer, MovimentoEstoqueSerializer,
    MovimentoEstoqueCreateSerializer, ReceitaProdutoSerializer
)

class UnidadeMedidaViewSet(viewsets.ModelViewSet):
    queryset = UnidadeMedida.objects.all()
    serializer_class = UnidadeMedidaSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nome', 'sigla']

class IngredienteViewSet(viewsets.ModelViewSet):
    queryset = Ingrediente.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['ativo', 'unidade_medida']
    search_fields = ['nome']
    ordering_fields = ['nome', 'quantidade_estoque']
    ordering = ['nome']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return IngredienteListSerializer
        return IngredienteDetailSerializer
    
    @action(detail=False, methods=['get'])
    def estoque_baixo(self, request):
        ingredientes = self.queryset.filter(
            quantidade_estoque__lte=models.F('estoque_minimo'),
            ativo=True
        )
        serializer = IngredienteListSerializer(ingredientes, many=True)
        return Response(serializer.data)

class MovimentoEstoqueViewSet(viewsets.ModelViewSet):
    queryset = MovimentoEstoque.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['ingrediente', 'tipo']
    ordering = ['-data']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return MovimentoEstoqueCreateSerializer
        return MovimentoEstoqueSerializer
    
    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)

class ReceitaProdutoViewSet(viewsets.ModelViewSet):
    queryset = ReceitaProduto.objects.all()
    serializer_class = ReceitaProdutoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['produto', 'ingrediente']