from django.core.cache import cache
from django.conf import settings
from functools import wraps
import hashlib
import json

def make_cache_key(*args, **kwargs):
    """Gera uma chave de cache única baseada nos argumentos"""
    key_parts = [str(arg) for arg in args]
    key_parts.extend([f"{k}:{v}" for k, v in sorted(kwargs.items())])
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