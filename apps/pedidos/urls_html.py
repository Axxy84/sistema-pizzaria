from django.urls import path
from . import views_html

app_name = 'pedidos'

urlpatterns = [
    # Lista de pedidos
    path('', views_html.PedidoListView.as_view(), name='pedido_list'),
    
    # CRUD
    path('novo/', views_html.PedidoCreateView.as_view(), name='pedido_create'),
    path('<int:pk>/', views_html.PedidoDetailView.as_view(), name='pedido_detail'),
    path('<int:pk>/editar/', views_html.PedidoUpdateView.as_view(), name='pedido_update'),
    path('<int:pk>/cancelar/', views_html.pedido_cancelar, name='pedido_cancel'),
    
    # Atualização de status
    path('<int:pk>/status/', views_html.pedido_atualizar_status, name='pedido_update_status'),
    
    # Views especiais
    path('<int:pk>/imprimir/', views_html.pedido_imprimir, name='pedido_print'),
    
    # AJAX endpoints
    path('ajax/buscar-cliente/', views_html.ajax_buscar_cliente, name='ajax_buscar_cliente'),
    path('ajax/buscar-produtos/', views_html.ajax_buscar_produtos, name='ajax_buscar_produtos'),
    path('ajax/calcular-taxa-entrega/', views_html.ajax_calcular_taxa_entrega, name='ajax_calcular_taxa_entrega'),
    path('ajax/cliente/<int:cliente_id>/enderecos/', views_html.ajax_cliente_enderecos, name='ajax_cliente_enderecos'),
]