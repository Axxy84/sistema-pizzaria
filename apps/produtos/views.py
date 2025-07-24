from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from apps.core.cache_utils import CachedViewSetMixin, cache_result, CacheManager
from .models import Categoria, Tamanho, Produto, ProdutoPreco
from .serializers import (
    CategoriaSerializer, TamanhoSerializer,
    ProdutoListSerializer, ProdutoDetailSerializer,
    ProdutoPrecoSerializer
)

class CategoriaViewSet(CachedViewSetMixin, viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['ativo']
    search_fields = ['nome']
    # Cache por 1 hora para categorias (mudam pouco)
    cache_timeout = 3600
    cache_type = 'produtos'

class TamanhoViewSet(CachedViewSetMixin, viewsets.ModelViewSet):
    queryset = Tamanho.objects.all()
    serializer_class = TamanhoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['ativo']
    # Cache por 1 hora para tamanhos (mudam pouco)
    cache_timeout = 3600
    cache_type = 'produtos'

class ProdutoViewSet(CachedViewSetMixin, viewsets.ModelViewSet):
    queryset = Produto.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['categoria', 'ativo']
    search_fields = ['nome', 'descricao']
    ordering_fields = ['nome', 'criado_em']
    ordering = ['nome']
    # Cache por 5 minutos para produtos
    cache_timeout = 300
    cache_type = 'produtos'
    
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
        import time
        start_time = time.time()
        
        produtos_por_categoria = {
            'pizzas': [],
            'bebidas': [],
            'bordas': []
        }
        
        # Buscar produtos ativos com seus preços
        produtos = Produto.objects.filter(ativo=True).select_related('categoria').prefetch_related(
            'precos__tamanho'
        ).order_by('categoria__nome', 'nome')
        
        query_time = time.time() - start_time
        print(f"[PRODUTOS] Query time: {query_time:.3f}s")
        
        # Tentar pegar do cache primeiro
        cache_key = 'produtos:para_pedido:v2'
        cached_data = cache.get(cache_key)
        
        if cached_data:
            print(f"[PRODUTOS] Retornando dados do cache")
            return Response(cached_data)
        
        for produto in produtos:
            categoria_key = self._mapear_categoria_para_aba(produto.categoria.nome if produto.categoria else '')
            
            if categoria_key is None or categoria_key not in produtos_por_categoria:
                continue
                
            if produto.tipo_produto == 'pizza' or 'pizza' in produto.categoria.nome.lower():
                # Para pizzas, incluir tamanhos
                tamanhos = []
                for preco in produto.precos.all():
                    tamanhos.append({
                        'id': preco.tamanho.id if preco.tamanho else preco.id,
                        'nome': preco.tamanho.nome if preco.tamanho else 'Único',
                        'size': preco.tamanho.nome if preco.tamanho else 'Único',
                        'preco': float(preco.preco_final)
                    })
                
                # Se não tem preços por tamanho, usar preço unitário
                if not tamanhos and produto.preco_unitario:
                    tamanhos.append({
                        'id': 0,
                        'nome': 'Único',
                        'size': 'Único',
                        'preco': float(produto.preco_unitario)
                    })
                
                produtos_por_categoria[categoria_key].append({
                    'id': produto.id,
                    'nome': produto.nome,
                    'descricao': produto.ingredientes or produto.descricao or '',
                    'ingredientes': produto.ingredientes or produto.descricao or '',
                    'tamanhos': tamanhos,
                    'tipo': 'pizza'
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
                    'descricao': produto.descricao or '',
                    'preco': preco,
                    'tipo': 'simples'
                })
        
        # Cachear por 30 minutos
        cache.set(cache_key, produtos_por_categoria, 60 * 30)
        
        total_time = time.time() - start_time
        print(f"[PRODUTOS] Total processing time: {total_time:.3f}s")
        
        return Response(produtos_por_categoria)
    
    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def para_pedido_rapido(self, request):
        """
        Endpoint otimizado para o novo sistema de pedido rápido
        Retorna produtos com estrutura simplificada
        """
        import time
        start_time = time.time()
        
        # Verificar cache primeiro
        cache_key = 'produtos:pedido_rapido:v1'
        cached_data = cache.get(cache_key)
        
        if cached_data:
            print(f"[PRODUTOS RAPIDO] Retornando do cache")
            return Response(cached_data)
        
        produtos = []
        
        # Otimizar query com select_related e prefetch_related
        queryset = Produto.objects.filter(ativo=True).select_related('categoria').prefetch_related(
            'precos__tamanho'
        ).order_by('categoria__nome', 'nome')
        
        print(f"[PRODUTOS RAPIDO] Query time: {time.time() - start_time:.3f}s")
        
        for produto in queryset:
            categoria_key = 'outros'
            if produto.categoria:
                categoria_key = self._mapear_categoria_para_aba(produto.categoria.nome)
            
            # Preparar preços
            precos = []
            for preco in produto.precos.all():
                precos.append({
                    'id': preco.id,
                    'tamanho': preco.tamanho.nome if preco.tamanho else 'Único',
                    'preco': float(preco.preco_final)
                })
            
            # Se não tiver preços com tamanho, usar preço unitário
            if not precos and hasattr(produto, 'preco_unitario') and produto.preco_unitario:
                precos.append({
                    'id': None,
                    'tamanho': 'Único',
                    'preco': float(produto.preco_unitario)
                })
            
            produtos.append({
                'id': produto.id,
                'nome': produto.nome,
                'descricao': produto.descricao,
                'categoria': categoria_key,
                'precos': precos
            })
        
        response_data = {'produtos': produtos}
        
        # Cachear por 30 minutos
        cache.set(cache_key, response_data, 60 * 30)
        
        total_time = time.time() - start_time
        print(f"[PRODUTOS RAPIDO] Total time: {total_time:.3f}s")
        
        return Response(response_data)
    
    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def para_mesa(self, request):
        """
        Endpoint simples para adicionar itens às mesas
        Retorna lista linear de produtos com preços
        """
        produtos_lista = []
        
        for produto in Produto.objects.filter(ativo=True).prefetch_related('precos__tamanho', 'categoria'):
            # Para cada preço do produto
            for preco in produto.precos.all():
                produtos_lista.append({
                    'id': produto.id,
                    'nome': produto.nome,
                    'categoria': produto.categoria.nome if produto.categoria else 'Outros',
                    'precos': [{
                        'produto_preco_id': preco.id,
                        'tamanho': preco.tamanho.nome if preco.tamanho else 'Único',
                        'preco': float(preco.preco_final)
                    }]
                })
        
        # Agrupar produtos pelo nome para ter todos os tamanhos juntos
        produtos_agrupados = {}
        for item in produtos_lista:
            nome = item['nome']
            if nome not in produtos_agrupados:
                produtos_agrupados[nome] = {
                    'id': item['id'],
                    'nome': nome,
                    'categoria': item['categoria'],
                    'precos': []
                }
            produtos_agrupados[nome]['precos'].extend(item['precos'])
        
        return Response(list(produtos_agrupados.values()))
    
    def _mapear_categoria_para_aba(self, categoria_nome):
        """Mapear nome da categoria para aba do frontend"""
        categoria_lower = categoria_nome.lower()
        
        if 'pizza' in categoria_lower or 'especial' in categoria_lower or 'tradicional' in categoria_lower:
            return 'pizzas'
        elif any(palavra in categoria_lower for palavra in ['bebida', 'refrigerante', 'suco', 'água', 'cerveja', 'drink']):
            return 'bebidas'
        elif any(palavra in categoria_lower for palavra in ['borda', 'recheada', 'adicional']):
            return 'bordas'
        else:
            # Sobremesas e outros produtos vão para "outros"
            return 'outros'

class ProdutoPrecoViewSet(CachedViewSetMixin, viewsets.ModelViewSet):
    queryset = ProdutoPreco.objects.all()
    serializer_class = ProdutoPrecoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['produto', 'tamanho']
    # Cache por 15 minutos para preços
    cache_timeout = 900
    cache_type = 'produtos'