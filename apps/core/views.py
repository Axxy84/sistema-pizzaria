"""
Views para monitoramento e gerenciamento do cache
"""
from django.shortcuts import render
from django.http import JsonResponse
from django.core.cache import cache
from django.conf import settings
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from django.db import connection
import django
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


@require_http_methods(["GET"])
@never_cache
def health_check(request):
    """
    Endpoint de health check para o indicador de status
    Retorna informações sobre o estado do sistema
    """
    try:
        # Verificar conexão com banco de dados
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            db_status = "ok"
    except:
        db_status = "error"
    
    # Verificar cache
    try:
        cache.set('health_check', 'ok', 10)
        cache_status = "ok" if cache.get('health_check') == 'ok' else "error"
    except:
        cache_status = "error"
    
    # Informações do sistema
    try:
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        memory_info = process.memory_info()
        cpu_percent = process.cpu_percent(interval=0.1)
        
        system_info = {
            "memory_mb": round(memory_info.rss / 1024 / 1024, 2),
            "cpu_percent": round(cpu_percent, 2),
            "threads": process.num_threads(),
        }
    except:
        system_info = {
            "memory_mb": 0,
            "cpu_percent": 0,
            "threads": 0,
        }
    
    # Status geral
    all_ok = db_status == "ok" and cache_status == "ok"
    
    return JsonResponse({
        "status": "healthy" if all_ok else "degraded",
        "services": {
            "database": db_status,
            "cache": cache_status,
        },
        "system": system_info,
        "timestamp": str(timezone.now())
    })


@require_http_methods(["GET"])
def server_status_view(request):
    """
    View para página de status detalhado do servidor
    """
    import platform
    
    context = {
        "python_version": platform.python_version(),
        "django_version": django.get_version(),
        "system": platform.system(),
        "node": platform.node(),
        "uptime": get_uptime(),
        "current_time": timezone.now()
    }
    
    return render(request, 'core/server_status.html', context)


def get_uptime():
    """Calcula o uptime do processo"""
    try:
        import psutil
        import os
        from datetime import datetime
        
        process = psutil.Process(os.getpid())
        create_time = datetime.fromtimestamp(process.create_time())
        uptime = datetime.now() - create_time
        
        hours, remainder = divmod(uptime.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        return f"{uptime.days}d {hours}h {minutes}m {seconds}s"
    except:
        return "N/A"