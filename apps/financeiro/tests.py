from django.test import TestCase
from django.contrib.auth.models import User
from decimal import Decimal
from datetime import date, timedelta
from .models import Caixa, MovimentoCaixa, ContaPagar


class CaixaModelTest(TestCase):
    def setUp(self):
        """Configuração inicial para os testes"""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
    def test_criar_caixa(self):
        """Testa criação de um novo caixa"""
        caixa = Caixa.objects.create(
            usuario=self.user,
            valor_abertura=Decimal('100.00')
        )
        
        self.assertEqual(caixa.status, 'aberto')
        self.assertEqual(caixa.valor_abertura, Decimal('100.00'))
        self.assertIsNone(caixa.valor_fechamento)
        self.assertEqual(str(caixa), f"Caixa {caixa.data_abertura.strftime('%d/%m/%Y')} - testuser")
        
    def test_saldo_esperado(self):
        """Testa cálculo do saldo esperado"""
        caixa = Caixa.objects.create(
            usuario=self.user,
            valor_abertura=Decimal('100.00')
        )
        
        # Adicionar movimentos
        MovimentoCaixa.objects.create(
            caixa=caixa,
            tipo='entrada',
            categoria='venda',
            descricao='Venda 1',
            valor=Decimal('50.00'),
            usuario=self.user
        )
        
        MovimentoCaixa.objects.create(
            caixa=caixa,
            tipo='saida',
            categoria='sangria',
            descricao='Sangria',
            valor=Decimal('20.00'),
            usuario=self.user
        )
        
        # Saldo esperado: 100 + 50 - 20 = 130
        self.assertEqual(caixa.saldo_esperado, Decimal('130.00'))


class MovimentoCaixaTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.caixa = Caixa.objects.create(
            usuario=self.user,
            valor_abertura=Decimal('100.00')
        )
        
    def test_criar_movimento_entrada(self):
        """Testa criação de movimento de entrada"""
        movimento = MovimentoCaixa.objects.create(
            caixa=self.caixa,
            tipo='entrada',
            categoria='venda',
            descricao='Venda Pizza',
            valor=Decimal('35.90'),
            usuario=self.user
        )
        
        self.assertEqual(movimento.tipo, 'entrada')
        self.assertEqual(movimento.valor, Decimal('35.90'))
        self.assertEqual(str(movimento), "Entrada - Venda Pizza - R$ 35.90")


class ContaPagarTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
    def test_criar_conta_pagar(self):
        """Testa criação de conta a pagar"""
        conta = ContaPagar.objects.create(
            descricao='Aluguel Dezembro',
            categoria='aluguel',
            valor=Decimal('2500.00'),
            data_vencimento=date.today() + timedelta(days=10),
            criado_por=self.user
        )
        
        self.assertEqual(conta.status, 'pendente')
        self.assertFalse(conta.vencida)
        self.assertIsNone(conta.pago_por)
        
    def test_conta_vencida(self):
        """Testa propriedade vencida"""
        conta_vencida = ContaPagar.objects.create(
            descricao='Conta vencida',
            categoria='outros',
            valor=Decimal('100.00'),
            data_vencimento=date.today() - timedelta(days=1),
            criado_por=self.user
        )
        
        self.assertTrue(conta_vencida.vencida)
        
        # Conta paga não deve ser considerada vencida
        conta_vencida.status = 'pago'
        conta_vencida.save()
        self.assertFalse(conta_vencida.vencida)