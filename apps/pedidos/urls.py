from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'pedidos', views.PedidoViewSet)

app_name = 'pedidos'

urlpatterns = [
    path('', include(router.urls)),
    
    # Endpoints para meio a meio
    path('meio-a-meio/sabores/', views.sabores_disponiveis, name='sabores_disponiveis'),
    path('meio-a-meio/calcular-preco/', views.calcular_preco_meio_a_meio, name='calcular_preco_meio_a_meio'),
    path('meio-a-meio/criar-item/', views.criar_item_meio_a_meio, name='criar_item_meio_a_meio'),
    
    # Página de confirmação
    path('<int:pedido_id>/confirmacao/', views.pedido_confirmacao_view, name='pedido_confirmacao'),
    
    # URLs para mesas
    path('mesas/', views.mesas_abertas_view, name='mesas_abertas'),
    path('mesas/abrir/', views.abrir_mesa_view, name='abrir_mesa'),
    path('mesas/<int:mesa_id>/fechar/', views.fechar_mesa_view, name='fechar_mesa'),
    path('mesas/<int:mesa_id>/detalhes/', views.mesa_detalhes_view, name='mesa_detalhes'),
    path('mesas/<int:mesa_id>/adicionar-pedido/', views.adicionar_pedido_mesa_view, name='adicionar_pedido_mesa'),
    path('mesas/<int:mesa_id>/imprimir/', views.imprimir_comanda_view, name='imprimir_comanda'),
]