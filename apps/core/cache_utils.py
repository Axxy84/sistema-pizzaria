from django.core.cache import cache
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from functools import wraps
import hashlib
import json

# Tempo padrão de cache
CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

def make_cache_key(*args, **kwargs):
    """Gera uma chave de cache única baseada nos argumentos"""
    key_parts = []
    
    # Processa argumentos posicionais
    for arg in args:
        if isinstance(arg, (list, dict, tuple)):
            key_parts.append(hashlib.md5(json.dumps(arg, sort_keys=True).encode()).hexdigest()[:8])
        else:
            key_parts.append(str(arg))
    
    # Processa argumentos nomeados
    for k, v in sorted(kwargs.items()):
        if isinstance(v, (list, dict, tuple)):
            key_parts.append(f"{k}:{hashlib.md5(json.dumps(v, sort_keys=True).encode()).hexdigest()[:8]}")
        else:
            key_parts.append(f"{k}:{v}")
    
    key_string = ":".join(key_parts)
    return hashlib.md5(key_string.encode()).hexdigest()

def cache_result(timeout=300, key_prefix=""):
    """
    Decorator para cachear o resultado de uma função
    
    Args:
        timeout: Tempo em segundos para manter o cache (padrão: 5 minutos)
        key_prefix: Prefixo para a chave de cache
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Gera chave de cache
            cache_key = f"{key_prefix}:{func.__name__}:{make_cache_key(*args, **kwargs)}"
            
            # Tenta pegar do cache
            result = cache.get(cache_key)
            if result is not None:
                return result
            
            # Se não estiver no cache, executa a função
            result = func(*args, **kwargs)
            
            # Salva no cache
            cache.set(cache_key, result, timeout)
            
            return result
        return wrapper
    return decorator

def cache_query(timeout=300):
    """Decorator específico para queries do Django"""
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            # Gera chave baseada na query
            cache_key = f"query:{self.model.__name__}:{func.__name__}:{make_cache_key(*args, **kwargs)}"
            
            # Tenta pegar do cache
            result = cache.get(cache_key)
            if result is not None:
                return result
            
            # Executa a query
            result = func(self, *args, **kwargs)
            
            # Salva no cache
            cache.set(cache_key, result, timeout)
            
            return result
        return wrapper
    return decorator

def invalidate_cache_pattern(pattern):
    """Invalida todas as chaves de cache que correspondem ao padrão"""
    if hasattr(cache, '_cache'):
        # Para backends que suportam pattern deletion
        cache.delete_pattern(f"*{pattern}*")
    else:
        # Fallback: não faz nada se o backend não suportar
        pass

class CacheManager:
    """Gerenciador centralizado de cache com versionamento"""
    
    PREFIXES = {
        'produtos': 'produtos',
        'clientes': 'clientes', 
        'pedidos': 'pedidos',
        'financeiro': 'financeiro',
        'estoque': 'estoque',
        'dashboard': 'dashboard',
    }
    
    @classmethod
    def invalidate_type(cls, cache_type):
        """Invalida todo cache de um tipo específico usando versionamento"""
        if cache_type not in cls.PREFIXES:
            return False
        
        version_key = f"cache_version:{cache_type}"
        current_version = cache.get(version_key, 0)
        cache.set(version_key, current_version + 1)
        return True
    
    @classmethod
    def get_cache_key(cls, cache_type, key):
        """Gera chave de cache com versioning"""
        if cache_type not in cls.PREFIXES:
            return key
        
        version_key = f"cache_version:{cache_type}"
        version = cache.get(version_key, 0)
        return f"{cls.PREFIXES[cache_type]}:v{version}:{key}"
    
    @classmethod
    def get(cls, cache_type, key, default=None):
        """Pega valor do cache com versioning"""
        cache_key = cls.get_cache_key(cache_type, key)
        return cache.get(cache_key, default)
    
    @classmethod
    def set(cls, cache_type, key, value, timeout=CACHE_TTL):
        """Salva valor no cache com versioning"""
        cache_key = cls.get_cache_key(cache_type, key)
        return cache.set(cache_key, value, timeout)

def get_cached_or_compute(cache_key, compute_func, timeout=CACHE_TTL):
    """
    Implementa o padrão cache-aside
    
    Uso:
        produtos = get_cached_or_compute(
            'produtos_ativos',
            lambda: list(Produto.objects.filter(ativo=True)),
            timeout=300
        )
    """
    result = cache.get(cache_key)
    if result is None:
        result = compute_func()
        cache.set(cache_key, result, timeout)
    return result

# Cache keys padrão
CACHE_KEYS = {
    'produtos_count': 'produtos:count:tipo',
    'produtos_list': 'produtos:list',
    'dashboard_stats': 'dashboard:stats',
    'vendas_periodo': 'vendas:periodo',
    'produtos_ranking': 'produtos:ranking',
}

# Timeouts padrão (em segundos)
CACHE_TIMEOUTS = {
    'short': 60,        # 1 minuto
    'medium': 300,      # 5 minutos
    'long': 900,        # 15 minutos
    'hour': 3600,       # 1 hora
    'day': 86400,       # 1 dia
}

# Mixin para ViewSets com cache automático
class CachedViewSetMixin:
    """
    Adiciona cache automático em ViewSets
    
    Uso:
        class ProdutoViewSet(CachedViewSetMixin, viewsets.ModelViewSet):
            cache_timeout = 300
            cache_type = 'produtos'
    """
    cache_timeout = 300
    cache_type = None
    
    def list(self, request, *args, **kwargs):
        """Lista com cache"""
        if not self.cache_type:
            return super().list(request, *args, **kwargs)
        
        # Gera chave baseada nos query params
        cache_key = f"{self.cache_type}:list:{make_cache_key(**request.GET.dict())}"
        
        # Tenta cache
        cached_response = cache.get(cache_key)
        if cached_response:
            return cached_response
        
        # Computa resultado
        response = super().list(request, *args, **kwargs)
        
        # Salva no cache apenas se sucesso
        if response.status_code == 200:
            cache.set(cache_key, response, self.cache_timeout)
        
        return response
    
    def retrieve(self, request, *args, **kwargs):
        """Detalhe com cache"""
        if not self.cache_type:
            return super().retrieve(request, *args, **kwargs)
        
        pk = kwargs.get('pk')
        cache_key = f"{self.cache_type}:detail:{pk}"
        
        cached_response = cache.get(cache_key)
        if cached_response:
            return cached_response
        
        response = super().retrieve(request, *args, **kwargs)
        
        if response.status_code == 200:
            cache.set(cache_key, response, self.cache_timeout)
        
        return response
    
    def create(self, request, *args, **kwargs):
        """Invalida cache ao criar"""
        response = super().create(request, *args, **kwargs)
        if self.cache_type and response.status_code == 201:
            CacheManager.invalidate_type(self.cache_type)
        return response
    
    def update(self, request, *args, **kwargs):
        """Invalida cache ao atualizar"""
        response = super().update(request, *args, **kwargs)
        if self.cache_type and response.status_code in [200, 204]:
            CacheManager.invalidate_type(self.cache_type)
        return response
    
    def destroy(self, request, *args, **kwargs):
        """Invalida cache ao deletar"""
        response = super().destroy(request, *args, **kwargs)
        if self.cache_type and response.status_code == 204:
            CacheManager.invalidate_type(self.cache_type)
        return response