from django.urls import path
from . import views_html

app_name = 'estoque'

urlpatterns = [
    # Dashboard
    path('', views_html.estoque_dashboard, name='dashboard'),
    
    # Ingredientes
    path('ingredientes/', views_html.ingrediente_list, name='ingrediente_list'),
    path('ingredientes/criar/', views_html.ingrediente_create, name='ingrediente_create'),
    path('ingredientes/<int:pk>/', views_html.ingrediente_detail, name='ingrediente_detail'),
    path('ingredientes/<int:pk>/editar/', views_html.ingrediente_edit, name='ingrediente_edit'),
    
    # Movimentos
    path('movimentos/', views_html.movimento_list, name='movimento_list'),
    path('movimentos/criar/', views_html.movimento_create, name='movimento_create'),
    
    # Relatórios e filtros especiais
    path('estoque-baixo/', views_html.estoque_baixo, name='estoque_baixo'),
    path('relatorio-movimentos/', views_html.relatorio_movimentos, name='relatorio_movimentos'),
    
    # AJAX
    path('ajax/ingredientes/', views_html.ingrediente_ajax_search, name='ingrediente_ajax_search'),
]