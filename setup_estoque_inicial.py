#!/usr/bin/env python
"""
Script para criar dados iniciais do estoque
Cria unidades de medida, ingredientes e alguns movimentos de exemplo
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

def create_unidades_medida():
    """Criar unidades de medida básicas"""
    unidades = [
        ('Quilograma', 'kg'),
        ('Grama', 'g'),
        ('Litro', 'L'),
        ('Mililitro', 'ml'),
        ('Unidade', 'un'),
        ('Pacote', 'pct'),
        ('Lata', 'lata'),
        ('Fatia', 'fatia'),
        ('Colher de sopa', 'csp'),
        ('Colher de chá', 'cch'),
    ]
    
    for nome, sigla in unidades:
        unidade, created = UnidadeMedida.objects.get_or_create(
            sigla=sigla,
            defaults={'nome': nome}
        )
        if created:
            print(f"✓ Criada unidade: {unidade}")
        else:
            print(f"- Unidade já existe: {unidade}")

def create_ingredientes():
    """Criar ingredientes básicos para pizzaria"""
    # Buscar unidades de medida
    kg = UnidadeMedida.objects.get(sigla='kg')
    g = UnidadeMedida.objects.get(sigla='g')
    ml = UnidadeMedida.objects.get(sigla='ml')
    un = UnidadeMedida.objects.get(sigla='un')
    pct = UnidadeMedida.objects.get(sigla='pct')
    lata = UnidadeMedida.objects.get(sigla='lata')
    
    ingredientes = [
        # Massas e farinhas
        ('Farinha de Trigo', kg, Decimal('0'), Decimal('5'), Decimal('4.50')),
        ('Fermento Biológico', g, Decimal('100'), Decimal('50'), Decimal('0.02')),
        ('Açúcar', kg, Decimal('1'), Decimal('2'), Decimal('3.20')),
        ('Sal', kg, Decimal('0.5'), Decimal('1'), Decimal('2.80')),
        ('Óleo', ml, Decimal('200'), Decimal('500'), Decimal('0.01')),
        
        # Molhos e temperos
        ('Molho de Tomate', lata, Decimal('5'), Decimal('10'), Decimal('3.50')),
        ('Orégano', g, Decimal('50'), Decimal('20'), Decimal('0.08')),
        ('Manjericão', g, Decimal('30'), Decimal('20'), Decimal('0.12')),
        ('Alho', kg, Decimal('0.2'), Decimal('0.5'), Decimal('18.00')),
        ('Cebola', kg, Decimal('1.5'), Decimal('2'), Decimal('4.50')),
        
        # Queijos
        ('Mussarela', kg, Decimal('3'), Decimal('2'), Decimal('28.00')),
        ('Queijo Parmesão', kg, Decimal('0.5'), Decimal('1'), Decimal('45.00')),
        ('Catupiry', kg, Decimal('1'), Decimal('0.5'), Decimal('35.00')),
        ('Queijo Gorgonzola', kg, Decimal('0.3'), Decimal('0.5'), Decimal('55.00')),
        
        # Carnes
        ('Presunto', kg, Decimal('1.2'), Decimal('1'), Decimal('25.00')),
        ('Pepperoni', kg, Decimal('0.8'), Decimal('0.5'), Decimal('38.00')),
        ('Frango Desfiado', kg, Decimal('2'), Decimal('1'), Decimal('18.00')),
        ('Bacon', kg, Decimal('0.6'), Decimal('0.5'), Decimal('32.00')),
        ('Calabresa', kg, Decimal('1.5'), Decimal('1'), Decimal('22.00')),
        
        # Frutos do mar
        ('Camarão', kg, Decimal('0.3'), Decimal('0.5'), Decimal('65.00')),
        ('Atum', lata, Decimal('8'), Decimal('5'), Decimal('8.50')),
        
        # Vegetais
        ('Tomate', kg, Decimal('2'), Decimal('1'), Decimal('6.00')),
        ('Champignon', pct, Decimal('3'), Decimal('2'), Decimal('4.50')),
        ('Azeitona Preta', pct, Decimal('2'), Decimal('1'), Decimal('6.80')),
        ('Azeitona Verde', pct, Decimal('2'), Decimal('1'), Decimal('6.80')),
        ('Pimentão', kg, Decimal('1'), Decimal('0.5'), Decimal('7.50')),
        ('Milho', lata, Decimal('6'), Decimal('3'), Decimal('3.20')),
        ('Ervilha', lata, Decimal('4'), Decimal('2'), Decimal('3.50')),
        
        # Outros
        ('Ovo', un, Decimal('20'), Decimal('12'), Decimal('0.60')),
        ('Palmito', lata, Decimal('3'), Decimal('2'), Decimal('12.00')),
        ('Rúcula', pct, Decimal('2'), Decimal('1'), Decimal('3.50')),
    ]
    
    for nome, unidade, estoque, minimo, custo in ingredientes:
        ingrediente, created = Ingrediente.objects.get_or_create(
            nome=nome,
            defaults={
                'unidade_medida': unidade,
                'quantidade_estoque': estoque,
                'estoque_minimo': minimo,
                'custo_unitario': custo,
                'ativo': True
            }
        )
        if created:
            print(f"✓ Criado ingrediente: {ingrediente}")
        else:
            print(f"- Ingrediente já existe: {ingrediente}")

def create_movimentos_exemplo():
    """Criar alguns movimentos de exemplo"""
    # Buscar usuário admin
    try:
        user = get_user_model().objects.filter(is_superuser=True).first()
        if not user:
            print("❌ Erro: Nenhum superusuário encontrado. Crie um primeiro.")
            return
    except Exception as e:
        print(f"❌ Erro ao buscar usuário: {e}")
        return
    
    # Buscar alguns ingredientes para criar movimentos
    ingredientes = Ingrediente.objects.all()[:5]
    
    movimentos_exemplo = [
        # Entradas (compras)
        (ingredientes[0], 'entrada', Decimal('10'), 'Compra inicial'),
        (ingredientes[1], 'entrada', Decimal('500'), 'Compra inicial'),
        (ingredientes[2], 'entrada', Decimal('5'), 'Compra inicial'),
        
        # Saídas (uso em produtos)
        (ingredientes[0], 'saida', Decimal('2'), 'Produção de pizzas'),
        (ingredientes[1], 'saida', Decimal('50'), 'Produção de pizzas'),
        
        # Ajustes
        (ingredientes[2], 'ajuste', Decimal('0.5'), 'Correção de inventário'),
        
        # Perdas
        (ingredientes[3], 'perda', Decimal('0.1'), 'Produto vencido'),
    ]
    
    for ingrediente, tipo, quantidade, motivo in movimentos_exemplo:
        # Verificar se há estoque suficiente para saídas/perdas
        if tipo in ['saida', 'perda'] and ingrediente.quantidade_estoque < quantidade:
            print(f"⚠️  Pulando movimento {tipo} de {ingrediente.nome}: estoque insuficiente")
            continue
            
        movimento = MovimentoEstoque.objects.create(
            ingrediente=ingrediente,
            tipo=tipo,
            quantidade=quantidade,
            custo_unitario=ingrediente.custo_unitario,
            motivo=motivo,
            usuario=user
        )
        print(f"✓ Criado movimento: {movimento}")

def main():
    print("🏗️  Configurando dados iniciais do estoque...")
    print("\n1. Criando unidades de medida...")
    create_unidades_medida()
    
    print("\n2. Criando ingredientes...")
    create_ingredientes()
    
    print("\n3. Criando movimentos de exemplo...")
    create_movimentos_exemplo()
    
    print("\n✅ Dados iniciais do estoque criados com sucesso!")
    print("\nResumo:")
    print(f"- Unidades de medida: {UnidadeMedida.objects.count()}")
    print(f"- Ingredientes: {Ingrediente.objects.count()}")
    print(f"- Movimentos: {MovimentoEstoque.objects.count()}")
    print(f"- Ingredientes com estoque baixo: {Ingrediente.objects.filter(quantidade_estoque__lte=Decimal('0')).count()}")
    
    print("\n🌐 Acesse: http://127.0.0.1:8000/estoque/")

if __name__ == '__main__':
    main()