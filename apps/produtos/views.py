from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Categoria, Tamanho, Produto, ProdutoPreco
from .serializers import (
    CategoriaSerializer, TamanhoSerializer,
    ProdutoListSerializer, ProdutoDetailSerializer,
    ProdutoPrecoSerializer
)

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['ativo']
    search_fields = ['nome']

class TamanhoViewSet(viewsets.ModelViewSet):
    queryset = Tamanho.objects.all()
    serializer_class = TamanhoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['ativo']

class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['categoria', 'ativo']
    search_fields = ['nome', 'descricao']
    ordering_fields = ['nome', 'criado_em']
    ordering = ['nome']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ProdutoListSerializer
        return ProdutoDetailSerializer

class ProdutoPrecoViewSet(viewsets.ModelViewSet):
    queryset = ProdutoPreco.objects.all()
    serializer_class = ProdutoPrecoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['produto', 'tamanho']