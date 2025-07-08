from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Cliente, Endereco
from .serializers import (
    ClienteListSerializer, ClienteDetailSerializer,
    ClienteCreateSerializer, EnderecoSerializer
)

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nome', 'telefone', 'email', 'cpf']
    ordering_fields = ['nome', 'criado_em']
    ordering = ['nome']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ClienteListSerializer
        elif self.action == 'create':
            return ClienteCreateSerializer
        return ClienteDetailSerializer
    
    @action(detail=True, methods=['post'])
    def adicionar_endereco(self, request, pk=None):
        cliente = self.get_object()
        serializer = EnderecoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(cliente=cliente)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EnderecoViewSet(viewsets.ModelViewSet):
    queryset = Endereco.objects.all()
    serializer_class = EnderecoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['cliente', 'tipo']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        cliente_id = self.request.query_params.get('cliente', None)
        if cliente_id:
            queryset = queryset.filter(cliente_id=cliente_id)
        return queryset