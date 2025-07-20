# Generated manually to fix missing status field

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pedidos', '0007_mesa'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedido',
            name='status',
            field=models.CharField(
                choices=[
                    ('recebido', 'Recebido'),
                    ('preparando', 'Preparando'),
                    ('saindo', 'Saindo'),
                    ('entregue', 'Entregue'),
                    ('cancelado', 'Cancelado'),
                ],
                default='recebido',
                max_length=20
            ),
            preserve_default=True,
        ),
    ]