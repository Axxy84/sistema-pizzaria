"""
Configurações de performance para o Django
"""

# Query optimization decorators
from functools import wraps
from django.core.cache import cache
from django.db.models import QuerySet
import hashlib
import json


def cache_query(timeout=300):
    """
    Decorator para cachear resultados de queries
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Gerar chave única baseada nos argumentos
            cache_key = f"{func.__module__}.{func.__name__}"
            if args:
                cache_key += f"_{hashlib.md5(str(args).encode()).hexdigest()}"
            if kwargs:
                cache_key += f"_{hashlib.md5(json.dumps(kwargs, sort_keys=True).encode()).hexdigest()}"
            
            # Tentar obter do cache
            result = cache.get(cache_key)
            if result is not None:
                return result
            
            # Executar função e cachear resultado
            result = func(*args, **kwargs)
            cache.set(cache_key, result, timeout)
            return result
        return wrapper
    return decorator


def optimize_queryset(queryset):
    """
    Otimiza automaticamente um queryset baseado no modelo
    """
    model = queryset.model
    
    # Lista de campos relacionados comuns por modelo
    related_fields = {
        'Pedido': ['cliente', 'usuario'],
        'ItemPedido': ['pedido', 'produto'],
        'Produto': ['categoria'],
        'Endereco': ['cliente'],
    }
    
    model_name = model.__name__
    if model_name in related_fields:
        queryset = queryset.select_related(*related_fields[model_name])
    
    return queryset


# Middleware para otimização de queries
class QueryOptimizationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Desabilitar queries desnecessárias em requests de assets
        if request.path.startswith('/static/') or request.path.startswith('/media/'):
            return self.get_response(request)
        
        response = self.get_response(request)
        return response


# Configurações para melhorar performance
PERFORMANCE_SETTINGS = {
    # Database
    'USE_PERSISTENT_CONNECTIONS': True,
    'CONNECTION_MAX_AGE': 600,
    'AUTOCOMMIT': True,
    
    # Cache
    'CACHE_MIDDLEWARE_SECONDS': 300,
    'CACHE_MIDDLEWARE_KEY_PREFIX': 'pizzaria',
    
    # Sessions
    'SESSION_SAVE_EVERY_REQUEST': False,
    'SESSION_COOKIE_AGE': 86400,  # 1 dia
    
    # Static files
    'STATICFILES_CACHE_TIMEOUT': 86400 * 365,  # 1 ano
    
    # Templates
    'TEMPLATE_CACHE_TIMEOUT': 300,
}


# Funções auxiliares para views
def get_cached_stats():
    """
    Retorna estatísticas do dashboard com cache
    """
    @cache_query(timeout=60)  # Cache por 1 minuto
    def _get_stats():
        from apps.produtos.models import Produto
        from apps.clientes.models import Cliente
        from apps.pedidos.models import Pedido
        from django.db.models import Sum
        from django.utils import timezone
        
        return {
            'total_produtos': Produto.objects.filter(ativo=True).count(),
            'total_clientes': Cliente.objects.filter(ativo=True).count(),
            'total_pedidos': Pedido.objects.count(),
            'pedidos_hoje': Pedido.objects.filter(
                criado_em__date=timezone.now().date()
            ).count(),
            'faturamento_hoje': Pedido.objects.filter(
                criado_em__date=timezone.now().date()
            ).exclude(status='cancelado').aggregate(
                total=Sum('total')
            )['total'] or 0
        }
    
    return _get_stats()