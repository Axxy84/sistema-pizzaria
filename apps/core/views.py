"""
Views para monitoramento e gerenciamento do cache
"""
from django.shortcuts import render
from django.http import JsonResponse
from django.core.cache import cache
from django.conf import settings
from django.views.decorators.cache import never_cache
from apps.core.cache_utils import CacheManager


@never_cache
def cache_status(request):
    """View para monitorar o status do cache (apenas em DEBUG)"""
    if not settings.DEBUG:
        return JsonResponse({'error': 'Not available in production'}, status=403)
    
    # Coleta informações do cache
    cache_info = {
        'backend': settings.CACHES['default']['BACKEND'],
        'timeout': settings.CACHES['default'].get('TIMEOUT', 300),
        'location': settings.CACHES['default'].get('LOCATION', 'memory'),
        'options': settings.CACHES['default'].get('OPTIONS', {}),
    }
    
    # Estatísticas se disponível
    stats = {}
    try:
        if hasattr(cache, '_cache'):
            backend = cache._cache
            if hasattr(backend, '_cache'):
                stats['entries'] = len(backend._cache)
                stats['max_entries'] = backend._max_entries if hasattr(backend, '_max_entries') else 'N/A'
            if hasattr(backend, '_cull_frequency'):
                stats['cull_frequency'] = backend._cull_frequency
    except:
        pass
    
    # Versões de cache por tipo
    versions = {}
    for cache_type in CacheManager.PREFIXES:
        version_key = f"cache_version:{cache_type}"
        versions[cache_type] = cache.get(version_key, 0)
    
    data = {
        'cache_info': cache_info,
        'statistics': stats,
        'versions': versions,
        'types': list(CacheManager.PREFIXES.keys()),
    }
    
    return JsonResponse(data)


@never_cache
def clear_cache(request):
    """API para limpar cache (apenas em DEBUG)"""
    if not settings.DEBUG:
        return JsonResponse({'error': 'Not available in production'}, status=403)
    
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    cache_type = request.POST.get('type', 'all')
    
    try:
        if cache_type == 'all':
            cache.clear()
            message = 'Todo o cache foi limpo'
        else:
            if CacheManager.invalidate_type(cache_type):
                message = f'Cache "{cache_type}" foi invalidado'
            else:
                return JsonResponse({'error': f'Tipo inválido: {cache_type}'}, status=400)
        
        return JsonResponse({
            'success': True,
            'message': message
        })
    except Exception as e:
        return JsonResponse({
            'error': str(e)
        }, status=500)


def cache_test(request):
    """View para testar o funcionamento do cache"""
    if not settings.DEBUG:
        return JsonResponse({'error': 'Not available in production'}, status=403)
    
    import time
    
    # Teste de escrita e leitura
    test_key = 'cache_test_key'
    test_value = {'timestamp': time.time(), 'message': 'Cache funcionando!'}
    
    # Escreve no cache
    cache.set(test_key, test_value, 60)
    
    # Lê do cache
    cached_value = cache.get(test_key)
    
    # Testa invalidação por tipo
    CacheManager.set('produtos', 'test_product', {'id': 1, 'name': 'Test'}, 60)
    product_before = CacheManager.get('produtos', 'test_product')
    
    CacheManager.invalidate_type('produtos')
    product_after = CacheManager.get('produtos', 'test_product')
    
    # Limpa teste
    cache.delete(test_key)
    
    return JsonResponse({
        'write_test': test_value,
        'read_test': cached_value,
        'match': test_value == cached_value,
        'invalidation_test': {
            'before': product_before,
            'after': product_after,
            'invalidated': product_after is None
        }
    })