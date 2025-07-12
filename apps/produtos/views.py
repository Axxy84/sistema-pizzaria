from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
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
    
    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def para_pedido(self, request):
        """
        Endpoint otimizado para buscar produtos por categoria no formato
        esperado pelo formulário de pedidos
        """
        produtos_por_categoria = {
            'pizzas': [],
            'bebidas': [],
            'bordas': []
        }
        
        # Buscar produtos ativos com seus preços
        produtos = Produto.objects.filter(ativo=True).select_related('categoria').prefetch_related(
            'precos__tamanho'
        ).order_by('categoria__nome', 'nome')
        
        for produto in produtos:
            categoria_key = self._mapear_categoria_para_aba(produto.categoria.nome if produto.categoria else '')
            
            if categoria_key is None or categoria_key not in produtos_por_categoria:
                continue
                
            if produto.tipo_produto == 'pizza' or 'pizza' in produto.categoria.nome.lower():
                # Para pizzas, incluir tamanhos
                tamanhos = []
                for preco in produto.precos.all():
                    tamanhos.append({
                        'size': preco.tamanho.nome if preco.tamanho else 'Único',
                        'preco': float(preco.preco_final)
                    })
                
                # Se não tem preços por tamanho, usar preço unitário
                if not tamanhos and produto.preco_unitario:
                    tamanhos.append({
                        'size': 'Único',
                        'preco': float(produto.preco_unitario)
                    })
                
                produtos_por_categoria[categoria_key].append({
                    'id': produto.id,
                    'nome': produto.nome,
                    'ingredientes': produto.ingredientes or produto.descricao or '',
                    'tamanhos': tamanhos
                })
            else:
                # Para outros produtos, usar preço simples
                preco = 0
                if produto.preco_unitario:
                    preco = float(produto.preco_unitario)
                elif produto.precos.exists():
                    preco = float(produto.precos.first().preco_final)
                
                produtos_por_categoria[categoria_key].append({
                    'id': produto.id,
                    'nome': produto.nome,
                    'preco': preco
                })
        
        return Response(produtos_por_categoria)
    
    def _mapear_categoria_para_aba(self, categoria_nome):
        """Mapear nome da categoria para aba do frontend"""
        categoria_lower = categoria_nome.lower()
        
        if 'pizza' in categoria_lower:
            return 'pizzas'
        elif any(palavra in categoria_lower for palavra in ['bebida', 'refrigerante', 'suco', 'água', 'cerveja']):
            return 'bebidas'
        elif any(palavra in categoria_lower for palavra in ['borda', 'recheada']):
            return 'bordas'
        else:
            return None  # Não incluir produtos não mapeados

class ProdutoPrecoViewSet(viewsets.ModelViewSet):
    queryset = ProdutoPreco.objects.all()
    serializer_class = ProdutoPrecoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['produto', 'tamanho']