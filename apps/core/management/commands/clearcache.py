"""
Comando para limpar o cache do sistema
Uso: python manage.py clearcache [tipo]
"""
from django.core.management.base import BaseCommand
from django.core.cache import cache
from apps.core.cache_utils import CacheManager


class Command(BaseCommand):
    help = 'Limpa o cache do sistema'
    
    def add_arguments(self, parser):
        parser.add_argument(
            'cache_type',
            nargs='?',
            type=str,
            default='all',
            help='Tipo de cache para limpar (produtos, clientes, pedidos, etc) ou "all" para limpar tudo'
        )
        
        parser.add_argument(
            '--stats',
            action='store_true',
            help='Mostra estatísticas do cache antes de limpar'
        )
    
    def handle(self, *args, **options):
        cache_type = options['cache_type']
        show_stats = options['stats']
        
        if show_stats:
            self.show_cache_stats()
        
        if cache_type == 'all':
            self.clear_all_cache()
        else:
            self.clear_cache_type(cache_type)
    
    def show_cache_stats(self):
        """Mostra estatísticas do cache se disponível"""
        self.stdout.write("\nEstatísticas do Cache:")
        self.stdout.write("-" * 40)
        
        try:
            if hasattr(cache, '_cache'):
                backend = cache._cache
                if hasattr(backend, '_cache'):
                    self.stdout.write(f"Entradas no cache: {len(backend._cache)}")
                if hasattr(backend, '_hits'):
                    self.stdout.write(f"Cache hits: {backend._hits}")
                if hasattr(backend, '_misses'):
                    self.stdout.write(f"Cache misses: {backend._misses}")
            else:
                self.stdout.write("Estatísticas não disponíveis para este backend")
        except:
            self.stdout.write("Erro ao obter estatísticas")
        
        self.stdout.write("-" * 40 + "\n")
    
    def clear_all_cache(self):
        """Limpa todo o cache"""
        self.stdout.write("Limpando todo o cache...")
        
        try:
            cache.clear()
            self.stdout.write(self.style.SUCCESS("✓ Cache limpo com sucesso!"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"✗ Erro ao limpar cache: {e}"))
    
    def clear_cache_type(self, cache_type):
        """Limpa cache de um tipo específico"""
        self.stdout.write(f"Limpando cache do tipo '{cache_type}'...")
        
        valid_types = list(CacheManager.PREFIXES.keys())
        
        if cache_type not in valid_types:
            self.stdout.write(self.style.ERROR(
                f"✗ Tipo inválido. Tipos válidos: {', '.join(valid_types)}"
            ))
            return
        
        try:
            CacheManager.invalidate_type(cache_type)
            self.stdout.write(self.style.SUCCESS(
                f"✓ Cache '{cache_type}' invalidado com sucesso!"
            ))
        except Exception as e:
            self.stdout.write(self.style.ERROR(
                f"✗ Erro ao invalidar cache '{cache_type}': {e}"
            ))