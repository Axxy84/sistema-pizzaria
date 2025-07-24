"""
Template tags para cache de fragmentos
Facilita o cache de partes específicas dos templates
"""
from django import template
from django.core.cache import cache
from django.template import Context, Template
from django.utils.safestring import mark_safe
from apps.core.cache_utils import make_cache_key, CACHE_TIMEOUTS

register = template.Library()


@register.simple_tag(takes_context=True)
def cache_fragment(context, fragment_name, timeout=None, *vary_on):
    """
    Cache de fragmento de template com suporte a variações
    
    Uso:
        {% cache_fragment "produto_card" 300 produto.id %}
            <div class="product-card">
                {{ produto.nome }}
            </div>
        {% endcache_fragment %}
    """
    # Gera chave de cache
    cache_key = make_cache_key(f"template_fragment:{fragment_name}", *vary_on)
    
    # Tenta pegar do cache
    fragment = cache.get(cache_key)
    if fragment is not None:
        return mark_safe(fragment)
    
    # Se não tem no cache, retorna placeholder
    # O conteúdo real será processado pelo tag endcache_fragment
    return f'<!-- CACHE_FRAGMENT_START:{cache_key}:{timeout or CACHE_TIMEOUTS["medium"]} -->'


@register.simple_tag
def endcache_fragment():
    """Marca o fim de um fragmento cacheável"""
    return '<!-- CACHE_FRAGMENT_END -->'


@register.simple_tag
def cache_bust(cache_type):
    """
    Invalida cache de um tipo específico
    
    Uso:
        {% cache_bust "produtos" %}
    """
    from apps.core.cache_utils import CacheManager
    CacheManager.invalidate_type(cache_type)
    return ''


@register.filter
def cache_key(value, prefix=''):
    """
    Gera uma chave de cache para um valor
    
    Uso:
        {{ produto.id|cache_key:"produto" }}
    """
    return make_cache_key(prefix, value)


@register.inclusion_tag('core/cache_info.html')
def cache_info():
    """
    Mostra informações sobre o cache (apenas em DEBUG)
    """
    from django.conf import settings
    
    if not settings.DEBUG:
        return {'show': False}
    
    # Pega estatísticas do cache se disponível
    stats = {}
    try:
        if hasattr(cache, '_cache'):
            stats = {
                'hits': getattr(cache._cache, '_hits', 0),
                'misses': getattr(cache._cache, '_misses', 0),
                'size': len(cache._cache._cache) if hasattr(cache._cache, '_cache') else 0,
            }
    except:
        pass
    
    return {
        'show': True,
        'backend': settings.CACHES['default']['BACKEND'],
        'stats': stats,
    }


# Context processor para processar fragmentos de cache
class CacheFragmentProcessor:
    """Processa fragmentos de cache em templates renderizados"""
    
    @staticmethod
    def process(content):
        """Processa o conteúdo e cacheia fragmentos marcados"""
        import re
        
        # Pattern para encontrar fragmentos de cache
        pattern = r'<!-- CACHE_FRAGMENT_START:([^:]+):(\d+) -->(.*?)<!-- CACHE_FRAGMENT_END -->'
        
        def replace_fragment(match):
            cache_key = match.group(1)
            timeout = int(match.group(2))
            fragment_content = match.group(3).strip()
            
            # Salva no cache
            cache.set(cache_key, fragment_content, timeout)
            
            return fragment_content
        
        # Substitui todos os fragmentos
        return re.sub(pattern, replace_fragment, content, flags=re.DOTALL)


# Middleware para processar fragmentos de cache
class CacheFragmentMiddleware:
    """
    Middleware que processa fragmentos de cache em responses HTML
    
    Adicionar em settings.py:
        MIDDLEWARE = [
            ...
            'apps.core.templatetags.cache_tags.CacheFragmentMiddleware',
        ]
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.get_response(request)
        
        # Processa apenas responses HTML
        if response.get('Content-Type', '').startswith('text/html'):
            try:
                content = response.content.decode('utf-8')
                processed = CacheFragmentProcessor.process(content)
                response.content = processed.encode('utf-8')
            except:
                pass
        
        return response