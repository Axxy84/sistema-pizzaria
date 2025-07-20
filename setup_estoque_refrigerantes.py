#!/usr/bin/env python
"""
Script para limpar estoque atual e criar apenas refrigerantes
"""
import os
import sys
import django
from decimal import Decimal

# Setup Django
sys.path.append('/home/labdev/Documentos/DjangoProject')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoProject.settings')
django.setup()

from apps.estoque.models import UnidadeMedida, Ingrediente, MovimentoEstoque
from django.contrib.auth.models import User

def limpar_estoque():
    """Limpar todos os ingredientes e movimentos atuais"""
    print("🧹 Limpando estoque atual...")
    
    # Deletar movimentos primeiro (por causa das foreign keys)
    movimentos_count = MovimentoEstoque.objects.count()
    MovimentoEstoque.objects.all().delete()
    print(f"   ✓ {movimentos_count} movimentos removidos")
    
    # Deletar ingredientes
    ingredientes_count = Ingrediente.objects.count()
    Ingrediente.objects.all().delete()
    print(f"   ✓ {ingredientes_count} ingredientes removidos")

def criar_refrigerantes():
    """Criar apenas ingredientes de refrigerantes"""
    print("🥤 Criando estoque de refrigerantes...")
    
    # Buscar unidades de medida
    try:
        litro = UnidadeMedida.objects.get(sigla='L')
        ml = UnidadeMedida.objects.get(sigla='ml')
        lata = UnidadeMedida.objects.get(sigla='lata')
        garrafa = UnidadeMedida.objects.get_or_create(nome='Garrafa', sigla='garrafa')[0]
    except UnidadeMedida.DoesNotExist:
        print("❌ Erro: Unidades de medida não encontradas. Execute setup_estoque_inicial.py primeiro.")
        return
    
    refrigerantes = [
        # (nome, unidade, estoque_atual, estoque_minimo, custo_unitario)
        ('Coca-Cola 350ml', lata, Decimal('24'), Decimal('12'), Decimal('2.50')),
        ('Coca-Cola 600ml', garrafa, Decimal('12'), Decimal('6'), Decimal('4.00')),
        ('Coca-Cola 2L', garrafa, Decimal('8'), Decimal('4'), Decimal('7.50')),
        
        ('Pepsi 350ml', lata, Decimal('18'), Decimal('12'), Decimal('2.30')),
        ('Pepsi 600ml', garrafa, Decimal('10'), Decimal('6'), Decimal('3.80')),
        ('Pepsi 2L', garrafa, Decimal('6'), Decimal('4'), Decimal('7.00')),
        
        ('Guaraná Antarctica 350ml', lata, Decimal('20'), Decimal('12'), Decimal('2.40')),
        ('Guaraná Antarctica 600ml', garrafa, Decimal('15'), Decimal('8'), Decimal('3.90')),
        ('Guaraná Antarctica 2L', garrafa, Decimal('10'), Decimal('5'), Decimal('7.80')),
        
        ('Fanta Laranja 350ml', lata, Decimal('16'), Decimal('10'), Decimal('2.50')),
        ('Fanta Laranja 600ml', garrafa, Decimal('8'), Decimal('5'), Decimal('4.00')),
        ('Fanta Laranja 2L', garrafa, Decimal('5'), Decimal('3'), Decimal('7.50')),
        
        ('Sprite 350ml', lata, Decimal('14'), Decimal('10'), Decimal('2.50')),
        ('Sprite 600ml', garrafa, Decimal('7'), Decimal('5'), Decimal('4.00')),
        ('Sprite 2L', garrafa, Decimal('4'), Decimal('3'), Decimal('7.50')),
        
        ('Água Mineral 500ml', garrafa, Decimal('30'), Decimal('20'), Decimal('1.50')),
        ('Água Mineral 1.5L', garrafa, Decimal('18'), Decimal('10'), Decimal('2.80')),
        
        ('Água com Gás 500ml', garrafa, Decimal('12'), Decimal('8'), Decimal('2.00')),
        
        ('Suco de Laranja 1L', garrafa, Decimal('8'), Decimal('5'), Decimal('5.50')),
        ('Suco de Uva 1L', garrafa, Decimal('6'), Decimal('4'), Decimal('6.00')),
        ('Suco de Maçã 1L', garrafa, Decimal('5'), Decimal('3'), Decimal('5.80')),
        
        ('Energético Red Bull 250ml', lata, Decimal('12'), Decimal('6'), Decimal('8.50')),
        ('Energético Monster 473ml', lata, Decimal('8'), Decimal('4'), Decimal('12.00')),
        
        ('Cerveja Skol 350ml', lata, Decimal('36'), Decimal('24'), Decimal('3.20')),
        ('Cerveja Brahma 350ml', lata, Decimal('30'), Decimal('18'), Decimal('3.50')),
        ('Cerveja Heineken 350ml', lata, Decimal('18'), Decimal('12'), Decimal('5.50')),
    ]
    
    for nome, unidade, estoque, minimo, custo in refrigerantes:
        ingrediente = Ingrediente.objects.create(
            nome=nome,
            unidade_medida=unidade,
            quantidade_estoque=estoque,
            estoque_minimo=minimo,
            custo_unitario=custo,
            ativo=True
        )
        print(f"   ✓ {ingrediente}")

def criar_movimentos_refrigerantes():
    """Criar alguns movimentos de exemplo para refrigerantes"""
    print("📦 Criando movimentos de exemplo...")
    
    try:
        user = User.objects.filter(is_superuser=True).first()
        if not user:
            print("   ⚠️  Nenhum superusuário encontrado. Pulando criação de movimentos.")
            return
    except Exception as e:
        print(f"   ❌ Erro ao buscar usuário: {e}")
        return
    
    # Pegar alguns refrigerantes para criar movimentos
    refrigerantes = Ingrediente.objects.all()[:5]
    
    movimentos_exemplo = [
        # Entradas (compras de refrigerantes)
        (refrigerantes[0], 'entrada', Decimal('48'), 'Compra de engradado - fornecedor XYZ'),
        (refrigerantes[1], 'entrada', Decimal('24'), 'Compra de garrafas - distribuidora ABC'),
        (refrigerantes[2], 'entrada', Decimal('12'), 'Compra de garrafas 2L - fornecedor XYZ'),
        
        # Saídas (vendas)
        (refrigerantes[0], 'saida', Decimal('6'), 'Vendas do dia - consumo balcão'),
        (refrigerantes[1], 'saida', Decimal('3'), 'Vendas delivery'),
        
        # Ajuste (correção de inventário)
        (refrigerantes[2], 'ajuste', Decimal('1'), 'Ajuste de inventário mensal'),
        
        # Perda (produto vencido/danificado)
        (refrigerantes[3], 'perda', Decimal('2'), 'Latas amassadas - descarte'),
    ]
    
    for ingrediente, tipo, quantidade, motivo in movimentos_exemplo:
        # Verificar estoque suficiente para saídas/perdas
        if tipo in ['saida', 'perda'] and ingrediente.quantidade_estoque < quantidade:
            print(f"   ⚠️  Pulando movimento {tipo} de {ingrediente.nome}: estoque insuficiente")
            continue
            
        movimento = MovimentoEstoque.objects.create(
            ingrediente=ingrediente,
            tipo=tipo,
            quantidade=quantidade,
            custo_unitario=ingrediente.custo_unitario,
            motivo=motivo,
            usuario=user
        )
        print(f"   ✓ {movimento}")

def main():
    print("🥤 Configurando estoque apenas com refrigerantes...")
    
    # Limpar estoque atual
    limpar_estoque()
    
    print("\n📝 Criando novos refrigerantes...")
    criar_refrigerantes()
    
    print("\n📦 Criando movimentos de exemplo...")
    criar_movimentos_refrigerantes()
    
    print("\n✅ Estoque de refrigerantes criado com sucesso!")
    
    # Estatísticas finais
    total_ingredientes = Ingrediente.objects.count()
    total_movimentos = MovimentoEstoque.objects.count()
    ingredientes_baixo = Ingrediente.objects.filter(
        quantidade_estoque__lte=Decimal('5')
    ).count()
    valor_total = sum(
        ing.quantidade_estoque * ing.custo_unitario 
        for ing in Ingrediente.objects.all()
    )
    
    print(f"\n📊 Resumo:")
    print(f"   • Refrigerantes cadastrados: {total_ingredientes}")
    print(f"   • Movimentos registrados: {total_movimentos}")
    print(f"   • Produtos com estoque baixo: {ingredientes_baixo}")
    print(f"   • Valor total do estoque: R$ {valor_total:.2f}")
    
    print(f"\n🌐 Acesse: http://127.0.0.1:8001/estoque/")

if __name__ == '__main__':
    main()