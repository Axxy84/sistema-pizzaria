from django.core.management.base import BaseCommand
from django.db import connection
from django.core.cache import cache
from django.conf import settings
import time

class Command(BaseCommand):
    help = 'Executa otimizações de performance no sistema'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear-cache',
            action='store_true',
            help='Limpa todo o cache Redis',
        )
        parser.add_argument(
            '--analyze-db',
            action='store_true',
            help='Executa ANALYZE nas tabelas principais',
        )
        parser.add_argument(
            '--check-indexes',
            action='store_true',
            help='Verifica uso de índices',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Iniciando otimizações de performance...'))
        
        if options['clear_cache']:
            self.clear_cache()
        
        if options['analyze_db']:
            self.analyze_database()
        
        if options['check_indexes']:
            self.check_indexes()
        
        # Se nenhuma opção específica, executar todas
        if not any([options['clear_cache'], options['analyze_db'], options['check_indexes']]):
            self.clear_cache()
            self.analyze_database()
            self.check_indexes()
            self.show_performance_tips()
        
        self.stdout.write(self.style.SUCCESS('Otimizações concluídas!'))

    def clear_cache(self):
        """Limpa o cache Redis"""
        self.stdout.write('Limpando cache...')
        try:
            cache.clear()
            self.stdout.write(self.style.SUCCESS('✓ Cache limpo com sucesso'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Erro ao limpar cache: {e}'))

    def analyze_database(self):
        """Executa ANALYZE nas tabelas principais"""
        self.stdout.write('Analisando tabelas do banco de dados...')
        
        tables = [
            'produtos_produto',
            'produtos_produtopreco',
            'produtos_categoria',
            'pedidos_pedido',
            'pedidos_itempedido',
            'clientes_cliente',
            'clientes_endereco',
        ]
        
        with connection.cursor() as cursor:
            for table in tables:
                try:
                    start_time = time.time()
                    cursor.execute(f'ANALYZE {table};')
                    elapsed = time.time() - start_time
                    self.stdout.write(
                        self.style.SUCCESS(f'✓ {table} analisada ({elapsed:.2f}s)')
                    )
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'✗ Erro ao analisar {table}: {e}')
                    )

    def check_indexes(self):
        """Verifica o uso de índices"""
        self.stdout.write('Verificando uso de índices...')
        
        # Query para verificar índices não utilizados
        query = """
        SELECT 
            schemaname,
            tablename,
            indexname,
            idx_scan,
            idx_tup_read,
            idx_tup_fetch
        FROM pg_stat_user_indexes
        WHERE schemaname = 'public'
        ORDER BY idx_scan ASC
        LIMIT 10;
        """
        
        with connection.cursor() as cursor:
            try:
                cursor.execute(query)
                results = cursor.fetchall()
                
                self.stdout.write('\nÍndices menos utilizados:')
                self.stdout.write('-' * 80)
                
                for row in results:
                    schema, table, index, scans, reads, fetches = row
                    if scans == 0:
                        self.stdout.write(
                            self.style.WARNING(
                                f'⚠ {index} em {table}: NUNCA USADO'
                            )
                        )
                    else:
                        self.stdout.write(
                            f'  {index} em {table}: {scans} scans'
                        )
                
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'✗ Erro ao verificar índices: {e}')
                )

    def show_performance_tips(self):
        """Mostra dicas de performance"""
        self.stdout.write('\n' + self.style.SUCCESS('Dicas de Performance:'))
        self.stdout.write('-' * 80)
        
        tips = [
            '1. Use select_related() e prefetch_related() nas queries',
            '2. Implemente paginação em listas grandes',
            '3. Use cache para dados que mudam pouco',
            '4. Evite queries N+1',
            '5. Use only() e defer() para campos específicos',
            '6. Configure CONN_MAX_AGE para reutilizar conexões',
            '7. Use bulk_create() e bulk_update() para operações em massa',
            '8. Monitore queries lentas com Django Debug Toolbar',
        ]
        
        for tip in tips:
            self.stdout.write(f'  {tip}')
        
        self.stdout.write('\n' + self.style.SUCCESS('Configurações atuais:'))
        self.stdout.write(f'  - DEBUG: {settings.DEBUG}')
        self.stdout.write(f'  - Cache Backend: {settings.CACHES["default"]["BACKEND"]}')
        self.stdout.write(f'  - Database: {settings.DATABASES["default"]["ENGINE"]}')