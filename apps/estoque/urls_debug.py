"""
URLs de debug para estoque - SEM autenticação
Apenas para testes durante desenvolvimento
"""
from django.urls import path
from . import views_debug

app_name = 'estoque_debug'

urlpatterns = [
    # Dashboard
    path('', views_debug.estoque_dashboard_debug, name='dashboard'),
    
    # Ingredientes
    path('ingredientes/', views_debug.ingrediente_list_debug, name='ingrediente_list'),
    path('ingredientes/<int:pk>/', views_debug.ingrediente_detail_debug, name='ingrediente_detail'),
    
    # Movimentos
    path('movimentos/', views_debug.movimento_list_debug, name='movimento_list'),
    
    # Relatórios e filtros especiais
    path('estoque-baixo/', views_debug.estoque_baixo_debug, name='estoque_baixo'),
]