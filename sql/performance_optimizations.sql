-- Script de Otimizações de Performance para PostgreSQL/Supabase
-- Execute este script para melhorar a performance do banco de dados

-- 1. Habilitar extensões úteis
CREATE EXTENSION IF NOT EXISTS pg_trgm; -- Para buscas de texto
CREATE EXTENSION IF NOT EXISTS btree_gist; -- Para índices compostos avançados

-- 2. Índices principais já criados via migration

-- 3. Estatísticas e configurações de tabelas
-- Aumentar estatísticas para colunas importantes
ALTER TABLE produtos_produto ALTER COLUMN tipo_produto SET STATISTICS 1000;
ALTER TABLE produtos_produto ALTER COLUMN ativo SET STATISTICS 1000;
ALTER TABLE pedidos_pedido ALTER COLUMN status SET STATISTICS 1000;
ALTER TABLE pedidos_pedido ALTER COLUMN criado_em SET STATISTICS 1000;

-- 4. Vacuum e Analyze das tabelas principais
VACUUM ANALYZE produtos_produto;
VACUUM ANALYZE produtos_produtopreco;
VACUUM ANALYZE produtos_categoria;
VACUUM ANALYZE pedidos_pedido;
VACUUM ANALYZE pedidos_itempedido;
VACUUM ANALYZE clientes_cliente;

-- 5. Configurações de autovacuum para tabelas com alta atividade
ALTER TABLE pedidos_pedido SET (
    autovacuum_vacuum_scale_factor = 0.1,
    autovacuum_analyze_scale_factor = 0.05
);

ALTER TABLE pedidos_itempedido SET (
    autovacuum_vacuum_scale_factor = 0.1,
    autovacuum_analyze_scale_factor = 0.05
);

-- 6. Views materializadas para relatórios (opcional)
-- CREATE MATERIALIZED VIEW IF NOT EXISTS mv_vendas_diarias AS
-- SELECT 
--     DATE(criado_em) as data,
--     COUNT(*) as total_pedidos,
--     SUM(total) as valor_total,
--     AVG(total) as ticket_medio
-- FROM pedidos_pedido
-- WHERE status = 'entregue'
-- GROUP BY DATE(criado_em)
-- ORDER BY data DESC;

-- CREATE INDEX idx_mv_vendas_data ON mv_vendas_diarias(data);

-- 7. Função para atualizar views materializadas (se criadas)
-- CREATE OR REPLACE FUNCTION refresh_materialized_views()
-- RETURNS void AS $$
-- BEGIN
--     REFRESH MATERIALIZED VIEW CONCURRENTLY mv_vendas_diarias;
-- END;
-- $$ LANGUAGE plpgsql;

-- 8. Configurações de conexão recomendadas (aplicar via Supabase Dashboard)
-- shared_buffers = 256MB
-- effective_cache_size = 1GB
-- work_mem = 4MB
-- maintenance_work_mem = 64MB
-- random_page_cost = 1.1
-- effective_io_concurrency = 200

-- 9. Monitoramento - Queries para verificar performance
-- Queries mais lentas:
-- SELECT query, calls, total_time, mean_time, max_time
-- FROM pg_stat_statements
-- ORDER BY mean_time DESC
-- LIMIT 20;

-- Índices não utilizados:
-- SELECT schemaname, tablename, indexname, idx_scan
-- FROM pg_stat_user_indexes
-- WHERE idx_scan = 0
-- ORDER BY schemaname, tablename;

-- Tamanho das tabelas:
-- SELECT 
--     schemaname,
--     tablename,
--     pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
-- FROM pg_tables
-- WHERE schemaname NOT IN ('pg_catalog', 'information_schema')
-- ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

-- 10. Limpeza de dados antigos (executar periodicamente)
-- DELETE FROM django_session WHERE expire_date < NOW() - INTERVAL '7 days';
-- DELETE FROM django_admin_log WHERE action_time < NOW() - INTERVAL '90 days';