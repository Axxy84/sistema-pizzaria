from django.urls import path
from django.views.generic import TemplateView
from . import views_html

app_name = 'pedidos'

urlpatterns = [
    # Lista de pedidos
    path('', views_html.PedidoListView.as_view(), name='pedido_list'),
    
    # CRUD
    path('novo/', views_html.PedidoCreateView.as_view(), name='pedido_create'),
    path('rapido/', views_html.PedidoRapidoView.as_view(), name='pedido_rapido'),
    path('test-produtos/', TemplateView.as_view(template_name='pedidos/test_produtos.html'), name='test_produtos'),
    path('<int:pk>/', views_html.PedidoDetailView.as_view(), name='pedido_detail'),
    path('<int:pk>/confirmacao/', views_html.PedidoDetailView.as_view(), name='pedido_confirmacao'),
    path('<int:pk>/editar/', views_html.PedidoUpdateView.as_view(), name='pedido_update'),
    path('<int:pk>/cancelar/', views_html.pedido_cancelar, name='pedido_cancel'),
    
    # Atualização de status
    path('<int:pk>/status/', views_html.pedido_atualizar_status, name='pedido_update_status'),
    path('<int:pk>/cancelar-com-senha/', views_html.pedido_cancelar_com_senha, name='pedido_cancelar_com_senha'),
    
    # Views especiais
    path('<int:pk>/imprimir/', views_html.pedido_imprimir, name='pedido_print'),
    path('<int:pk>/comanda-cozinha/', views_html.pedido_comanda_cozinha, name='pedido_comanda_cozinha'),
    
    # AJAX endpoints
    path('ajax/buscar-cliente/', views_html.ajax_buscar_cliente, name='ajax_buscar_cliente'),
    path('ajax/buscar-produtos/', views_html.ajax_buscar_produtos, name='ajax_buscar_produtos'),
    path('ajax/calcular-taxa-entrega/', views_html.ajax_calcular_taxa_entrega, name='ajax_calcular_taxa_entrega'),
    path('ajax/cliente/<int:cliente_id>/enderecos/', views_html.ajax_cliente_enderecos, name='ajax_cliente_enderecos'),
    
    # API do pedido rápido
    path('api/criar-rapido/', views_html.api_criar_pedido_rapido, name='api_criar_pedido_rapido'),
]