# Generated by Django 5.2.4 on 2025-07-12 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pedidos', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedido',
            name='status',
            field=models.CharField(choices=[('recebido', 'Recebido'), ('preparando', 'Preparando'), ('saindo', 'Saindo'), ('entregue', 'Entregue'), ('cancelado', 'Cancelado')], default='recebido', max_length=20),
        ),
    ]
