from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'pedidos', views.PedidoViewSet)

urlpatterns = [
    path('', include(router.urls)),
    
    # Endpoints para meio a meio
    path('meio-a-meio/sabores/', views.sabores_disponiveis, name='sabores_disponiveis'),
    path('meio-a-meio/calcular-preco/', views.calcular_preco_meio_a_meio, name='calcular_preco_meio_a_meio'),
    path('meio-a-meio/criar-item/', views.criar_item_meio_a_meio, name='criar_item_meio_a_meio'),
]