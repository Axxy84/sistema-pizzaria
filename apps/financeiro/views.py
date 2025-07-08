from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
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