# Generated by Django 5.2.4 on 2025-07-13 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pedidos', '0003_update_existing_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='itempedido',
            name='meio_a_meio_data',
            field=models.JSONField(blank=True, help_text='Dados da personalização meio a meio', null=True),
        ),
    ]
