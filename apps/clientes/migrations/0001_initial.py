# Generated by Django 5.2.4 on 2025-07-06 13:05

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=200)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('telefone', models.CharField(max_length=15, validators=[django.core.validators.RegexValidator(message="Número de telefone deve estar no formato: '+999999999'. Até 15 dígitos permitidos.", regex='^\\+?1?\\d{9,15}$')])),
                ('telefone2', models.CharField(blank=True, max_length=15, validators=[django.core.validators.RegexValidator(message="Número de telefone deve estar no formato: '+999999999'. Até 15 dígitos permitidos.", regex='^\\+?1?\\d{9,15}$')])),
                ('cpf', models.CharField(blank=True, max_length=14, null=True, unique=True)),
                ('data_nascimento', models.DateField(blank=True, null=True)),
                ('observacoes', models.TextField(blank=True)),
                ('ativo', models.BooleanField(default=True)),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('atualizado_em', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Cliente',
                'verbose_name_plural': 'Clientes',
                'ordering': ['nome'],
            },
        ),
        migrations.CreateModel(
            name='Endereco',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(choices=[('casa', 'Casa'), ('trabalho', 'Trabalho'), ('outro', 'Outro')], default='casa', max_length=20)),
                ('cep', models.CharField(max_length=9)),
                ('logradouro', models.CharField(max_length=200)),
                ('numero', models.CharField(max_length=20)),
                ('complemento', models.CharField(blank=True, max_length=100)),
                ('bairro', models.CharField(max_length=100)),
                ('cidade', models.CharField(max_length=100)),
                ('estado', models.CharField(max_length=2)),
                ('referencia', models.CharField(blank=True, max_length=200)),
                ('principal', models.BooleanField(default=False)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='enderecos', to='clientes.cliente')),
            ],
            options={
                'verbose_name': 'Endereço',
                'verbose_name_plural': 'Endereços',
                'ordering': ['-principal', 'tipo'],
            },
        ),
    ]
