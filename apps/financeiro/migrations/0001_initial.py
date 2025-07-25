# Generated by Django 5.2.4 on 2025-07-06 13:05

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('pedidos', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Caixa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('aberto', 'Aberto'), ('fechado', 'Fechado')], default='aberto', max_length=20)),
                ('valor_abertura', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('valor_fechamento', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('data_abertura', models.DateTimeField(auto_now_add=True)),
                ('data_fechamento', models.DateTimeField(blank=True, null=True)),
                ('observacoes_abertura', models.TextField(blank=True)),
                ('observacoes_fechamento', models.TextField(blank=True)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='caixas', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Caixa',
                'verbose_name_plural': 'Caixas',
                'ordering': ['-data_abertura'],
            },
        ),
        migrations.CreateModel(
            name='ContaPagar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.CharField(max_length=200)),
                ('categoria', models.CharField(choices=[('fornecedor', 'Fornecedor'), ('funcionario', 'Funcionário'), ('aluguel', 'Aluguel'), ('energia', 'Energia'), ('agua', 'Água'), ('internet', 'Internet'), ('outros', 'Outros')], max_length=20)),
                ('valor', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('data_vencimento', models.DateField()),
                ('data_pagamento', models.DateField(blank=True, null=True)),
                ('status', models.CharField(choices=[('pendente', 'Pendente'), ('pago', 'Pago'), ('cancelado', 'Cancelado')], default='pendente', max_length=20)),
                ('observacoes', models.TextField(blank=True)),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('criado_por', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='contas_criadas', to=settings.AUTH_USER_MODEL)),
                ('pago_por', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='contas_pagas', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Conta a Pagar',
                'verbose_name_plural': 'Contas a Pagar',
                'ordering': ['status', 'data_vencimento'],
            },
        ),
        migrations.CreateModel(
            name='MovimentoCaixa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(choices=[('entrada', 'Entrada'), ('saida', 'Saída')], max_length=20)),
                ('categoria', models.CharField(choices=[('venda', 'Venda'), ('sangria', 'Sangria'), ('suprimento', 'Suprimento'), ('despesa', 'Despesa'), ('outros', 'Outros')], max_length=20)),
                ('descricao', models.CharField(max_length=200)),
                ('valor', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('data', models.DateTimeField(auto_now_add=True)),
                ('caixa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='movimentos', to='financeiro.caixa')),
                ('pedido', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='movimentos_caixa', to='pedidos.pedido')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Movimento de Caixa',
                'verbose_name_plural': 'Movimentos de Caixa',
                'ordering': ['-data'],
            },
        ),
    ]
