from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Sum, Count
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView
from django.views import View
from datetime import date, timedelta
from .models import Caixa, MovimentoCaixa, ContaPagar
from .serializers import (
    CaixaListSerializer, CaixaDetailSerializer,
    CaixaOpenSerializer, CaixaCloseSerializer,
    MovimentoCaixaSerializer, ContaPagarListSerializer,
    ContaPagarDetailSerializer, ContaPagarPaySerializer
)

class CaixaViewSet(viewsets.ModelViewSet):
    queryset = Caixa.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status', 'usuario']
    ordering = ['-data_abertura']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return CaixaListSerializer
        elif self.action == 'abrir':
            return CaixaOpenSerializer
        elif self.action == 'fechar':
            return CaixaCloseSerializer
        return CaixaDetailSerializer
    
    @action(detail=False, methods=['get'])
    def caixa_aberto(self, request):
        caixa = self.queryset.filter(status='aberto').first()
        if caixa:
            serializer = CaixaDetailSerializer(caixa)
            return Response(serializer.data)
        return Response(
            {'detail': 'Nenhum caixa aberto'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    @action(detail=False, methods=['post'])
    def abrir(self, request):
        # Verifica se já existe caixa aberto
        if self.queryset.filter(status='aberto').exists():
            return Response(
                {'detail': 'Já existe um caixa aberto'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = CaixaOpenSerializer(data=request.data)
        if serializer.is_valid():
            caixa = Caixa.objects.create(
                usuario=request.user,
                **serializer.validated_data
            )
            return Response(
                CaixaDetailSerializer(caixa).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def fechar(self, request, pk=None):
        caixa = self.get_object()
        if caixa.status == 'fechado':
            return Response(
                {'detail': 'Caixa já está fechado'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = CaixaCloseSerializer(caixa, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(CaixaDetailSerializer(caixa).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MovimentoCaixaViewSet(viewsets.ModelViewSet):
    queryset = MovimentoCaixa.objects.all()
    serializer_class = MovimentoCaixaSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['caixa', 'tipo', 'categoria']
    ordering = ['-data']
    
    def perform_create(self, serializer):
        # Pega o caixa aberto
        caixa = Caixa.objects.filter(status='aberto').first()
        if not caixa:
            raise ValidationError({'detail': 'Nenhum caixa aberto'})
        
        serializer.save(usuario=self.request.user, caixa=caixa)

class ContaPagarViewSet(viewsets.ModelViewSet):
    queryset = ContaPagar.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status', 'categoria']
    ordering = ['status', 'data_vencimento']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ContaPagarListSerializer
        return ContaPagarDetailSerializer
    
    def perform_create(self, serializer):
        serializer.save(criado_por=self.request.user)
    
    @action(detail=True, methods=['post'])
    def pagar(self, request, pk=None):
        conta = self.get_object()
        if conta.status == 'pago':
            return Response(
                {'detail': 'Conta já está paga'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = ContaPagarPaySerializer(data=request.data)
        if serializer.is_valid():
            conta.status = 'pago'
            conta.data_pagamento = serializer.validated_data['data_pagamento']
            conta.pago_por = request.user
            if 'observacoes' in serializer.validated_data:
                conta.observacoes += f"\n\nPagamento: {serializer.validated_data['observacoes']}"
            conta.save()
            
            return Response(ContaPagarDetailSerializer(conta).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def vencidas(self, request):
        from datetime import date
        vencidas = self.queryset.filter(
            status='pendente',
            data_vencimento__lt=date.today()
        )
        serializer = ContaPagarListSerializer(vencidas, many=True)
        return Response(serializer.data)


# Template-based views for cash closing system
class CaixaDashboardView(View):
    """Dashboard principal do controle de caixa"""
    
    def get(self, request):
        # Busca caixa aberto
        caixa_aberto = Caixa.objects.filter(status='aberto').first()
        
        # Estatísticas do dia
        hoje = date.today()
        
        # Busca pedidos do dia para calcular vendas
        from apps.pedidos.models import Pedido
        pedidos_hoje = Pedido.objects.filter(
            criado_em__date=hoje,
            status='entregue'
        )
        
        # Calcula totais de vendas
        total_vendas = pedidos_hoje.aggregate(
            total=Sum('total')
        )['total'] or 0
        
        quantidade_pedidos = pedidos_hoje.count()
        
        # Calcula ticket médio
        ticket_medio = total_vendas / quantidade_pedidos if quantidade_pedidos > 0 else 0
        
        # Vendas por forma de pagamento
        vendas_por_pagamento = pedidos_hoje.values('forma_pagamento').annotate(
            total=Sum('total'),
            quantidade=Count('id')
        )
        
        # Despesas do dia
        if caixa_aberto:
            despesas_hoje = MovimentoCaixa.objects.filter(
                caixa=caixa_aberto,
                tipo='saida',
                data__date=hoje
            )
            total_despesas = despesas_hoje.aggregate(
                total=Sum('valor')
            )['total'] or 0
        else:
            despesas_hoje = MovimentoCaixa.objects.none()
            total_despesas = 0
        
        # Calcula lucro
        lucro_liquido = total_vendas - total_despesas
        margem_lucro = (lucro_liquido / total_vendas * 100) if total_vendas > 0 else 0
        
        context = {
            'caixa_aberto': caixa_aberto,
            'total_vendas': total_vendas,
            'quantidade_pedidos': quantidade_pedidos,
            'ticket_medio': ticket_medio,
            'vendas_por_pagamento': vendas_por_pagamento,
            'despesas_hoje': despesas_hoje,
            'total_despesas': total_despesas,
            'lucro_liquido': lucro_liquido,
            'margem_lucro': margem_lucro,
            'hoje': hoje,
        }
        
        return render(request, 'financeiro/dashboard.html', context)


class AbrirCaixaView(View):
    """View para abrir o caixa"""
    
    def get(self, request):
        # Verifica se já existe caixa aberto
        if Caixa.objects.filter(status='aberto').exists():
            messages.warning(request, 'Já existe um caixa aberto.')
            return redirect('financeiro:dashboard')
        
        return render(request, 'financeiro/abrir_caixa.html')
    
    def post(self, request):
        # Verifica se já existe caixa aberto
        if Caixa.objects.filter(status='aberto').exists():
            messages.error(request, 'Já existe um caixa aberto.')
            return redirect('financeiro:dashboard')
        
        saldo_inicial = request.POST.get('saldo_inicial', 0)
        observacoes = request.POST.get('observacoes', '')
        
        try:
            caixa = Caixa.objects.create(
                usuario=request.user,
                valor_abertura=float(saldo_inicial),
                observacoes_abertura=observacoes
            )
            messages.success(request, f'Caixa aberto com sucesso! Saldo inicial: R$ {saldo_inicial}')
            return redirect('financeiro:dashboard')
        except Exception as e:
            messages.error(request, f'Erro ao abrir caixa: {str(e)}')
            return render(request, 'financeiro/abrir_caixa.html')


class FecharCaixaView(View):
    """View para fechar o caixa com reconciliação"""
    
    def get(self, request):
        caixa = get_object_or_404(Caixa, status='aberto')
        
        # Busca movimentos do caixa
        movimentos = MovimentoCaixa.objects.filter(caixa=caixa)
        
        # Calcula totais
        total_entradas = movimentos.filter(tipo='entrada').aggregate(
            total=Sum('valor')
        )['total'] or 0
        
        total_saidas = movimentos.filter(tipo='saida').aggregate(
            total=Sum('valor')
        )['total'] or 0
        
        saldo_teorico = caixa.valor_abertura + total_entradas - total_saidas
        
        # Agrupa movimentos por categoria
        movimentos_por_categoria = movimentos.values('categoria', 'tipo').annotate(
            total=Sum('valor'),
            quantidade=Count('id')
        )
        
        context = {
            'caixa': caixa,
            'movimentos': movimentos.order_by('-data'),
            'total_entradas': total_entradas,
            'total_saidas': total_saidas,
            'saldo_teorico': saldo_teorico,
            'movimentos_por_categoria': movimentos_por_categoria,
        }
        
        return render(request, 'financeiro/fechar_caixa.html', context)
    
    def post(self, request):
        caixa = get_object_or_404(Caixa, status='aberto')
        
        saldo_final = request.POST.get('saldo_final')
        observacoes_fechamento = request.POST.get('observacoes_fechamento', '')
        
        try:
            # Calcula saldo teórico
            movimentos = MovimentoCaixa.objects.filter(caixa=caixa)
            total_entradas = movimentos.filter(tipo='entrada').aggregate(
                total=Sum('valor')
            )['total'] or 0
            total_saidas = movimentos.filter(tipo='saida').aggregate(
                total=Sum('valor')
            )['total'] or 0
            saldo_teorico = caixa.valor_abertura + total_entradas - total_saidas
            
            # Calcula diferença
            diferenca = float(saldo_final) - saldo_teorico
            
            # Fecha o caixa
            caixa.status = 'fechado'
            caixa.data_fechamento = timezone.now()
            caixa.saldo_final = float(saldo_final)
            caixa.diferenca = diferenca
            
            if observacoes_fechamento:
                if caixa.observacoes:
                    caixa.observacoes += f"\n\nFechamento: {observacoes_fechamento}"
                else:
                    caixa.observacoes = f"Fechamento: {observacoes_fechamento}"
            
            caixa.save()
            
            if abs(diferenca) > 0:
                messages.warning(
                    request, 
                    f'Caixa fechado com diferença de R$ {diferenca:.2f}. '
                    f'Saldo teórico: R$ {saldo_teorico:.2f}, Saldo informado: R$ {float(saldo_final):.2f}'
                )
            else:
                messages.success(request, 'Caixa fechado com sucesso! Valores conferem.')
            
            return redirect('financeiro:dashboard')
            
        except Exception as e:
            messages.error(request, f'Erro ao fechar caixa: {str(e)}')
            return self.get(request)


class AdicionarMovimentoView(View):
    """View para adicionar movimentos (despesas/receitas) ao caixa"""
    
    def get(self, request):
        caixa = Caixa.objects.filter(status='aberto').first()
        if not caixa:
            messages.error(request, 'Nenhum caixa aberto. Abra um caixa primeiro.')
            return redirect('financeiro:abrir_caixa')
        
        context = {'caixa': caixa}
        return render(request, 'financeiro/adicionar_movimento.html', context)
    
    def post(self, request):
        caixa = Caixa.objects.filter(status='aberto').first()
        if not caixa:
            messages.error(request, 'Nenhum caixa aberto.')
            return redirect('financeiro:abrir_caixa')
        
        try:
            movimento = MovimentoCaixa.objects.create(
                caixa=caixa,
                usuario=request.user,
                tipo=request.POST.get('tipo'),
                categoria=request.POST.get('categoria'),
                descricao=request.POST.get('descricao'),
                valor=float(request.POST.get('valor')),
                observacoes=request.POST.get('observacoes', '')
            )
            
            messages.success(
                request, 
                f'Movimento adicionado: {movimento.get_tipo_display()} - '
                f'{movimento.categoria} - R$ {movimento.valor:.2f}'
            )
            return redirect('financeiro:dashboard')
            
        except Exception as e:
            messages.error(request, f'Erro ao adicionar movimento: {str(e)}')
            return self.get(request)


class HistoricoCaixaView(ListView):
    """Lista histórico de caixas fechados"""
    
    model = Caixa
    template_name = 'financeiro/historico_caixa.html'
    context_object_name = 'caixas'
    paginate_by = 20
    
    def get_queryset(self):
        return Caixa.objects.filter(status='fechado').order_by('-data_fechamento')


class DetalhesCaixaView(DetailView):
    """Detalhes de um caixa específico"""
    
    model = Caixa
    template_name = 'financeiro/detalhes_caixa.html'
    context_object_name = 'caixa'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        caixa = self.get_object()
        
        # Busca movimentos do caixa
        movimentos = MovimentoCaixa.objects.filter(caixa=caixa).order_by('-data')
        
        # Agrupa por categoria
        movimentos_por_categoria = movimentos.values('categoria', 'tipo').annotate(
            total=Sum('valor'),
            quantidade=Count('id')
        )
        
        context.update({
            'movimentos': movimentos,
            'movimentos_por_categoria': movimentos_por_categoria,
        })
        
        return context