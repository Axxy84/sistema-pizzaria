# Generated manually for performance optimization

from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('produtos', '0001_initial'),
        ('pedidos', '0001_initial'),
        ('clientes', '0001_initial'),
    ]

    operations = [
        # Índices para Produtos
        migrations.RunSQL(
            "CREATE INDEX IF NOT EXISTS idx_produto_tipo_ativo ON produtos_produto(tipo_produto, ativo);",
            reverse_sql="DROP INDEX IF EXISTS idx_produto_tipo_ativo;"
        ),
        migrations.RunSQL(
            "CREATE INDEX IF NOT EXISTS idx_produto_nome_trgm ON produtos_produto USING gin(nome gin_trgm_ops);",
            reverse_sql="DROP INDEX IF EXISTS idx_produto_nome_trgm;",
            state_operations=[]
        ),
        migrations.RunSQL(
            "CREATE INDEX IF NOT EXISTS idx_produto_criado_em ON produtos_produto(criado_em DESC);",
            reverse_sql="DROP INDEX IF EXISTS idx_produto_criado_em;"
        ),
        
        # Índices para Pedidos
        migrations.RunSQL(
            "CREATE INDEX IF NOT EXISTS idx_pedido_status_criado ON pedidos_pedido(status, criado_em DESC);",
            reverse_sql="DROP INDEX IF EXISTS idx_pedido_status_criado;"
        ),
        migrations.RunSQL(
            "CREATE INDEX IF NOT EXISTS idx_pedido_cliente_criado ON pedidos_pedido(cliente_id, criado_em DESC);",
            reverse_sql="DROP INDEX IF EXISTS idx_pedido_cliente_criado;"
        ),
        migrations.RunSQL(
            "CREATE INDEX IF NOT EXISTS idx_pedido_tipo ON pedidos_pedido(tipo);",
            reverse_sql="DROP INDEX IF EXISTS idx_pedido_tipo;"
        ),
        
        # Índices para ItemPedido
        migrations.RunSQL(
            "CREATE INDEX IF NOT EXISTS idx_item_pedido_id ON pedidos_itempedido(pedido_id);",
            reverse_sql="DROP INDEX IF EXISTS idx_item_pedido_id;"
        ),
        migrations.RunSQL(
            "CREATE INDEX IF NOT EXISTS idx_item_produto_preco ON pedidos_itempedido(produto_preco_id);",
            reverse_sql="DROP INDEX IF EXISTS idx_item_produto_preco;"
        ),
        
        # Índices para ProdutoPreco
        migrations.RunSQL(
            "CREATE INDEX IF NOT EXISTS idx_produto_preco_produto ON produtos_produtopreco(produto_id, tamanho_id);",
            reverse_sql="DROP INDEX IF EXISTS idx_produto_preco_produto;"
        ),
        
        # Índices para Cliente
        migrations.RunSQL(
            "CREATE INDEX IF NOT EXISTS idx_cliente_telefone ON clientes_cliente(telefone);",
            reverse_sql="DROP INDEX IF EXISTS idx_cliente_telefone;"
        ),
        migrations.RunSQL(
            "CREATE INDEX IF NOT EXISTS idx_cliente_email ON clientes_cliente(email);",
            reverse_sql="DROP INDEX IF EXISTS idx_cliente_email;"
        ),
    ]