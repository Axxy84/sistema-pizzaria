from django.urls import path
from django.views.generic import TemplateView
from . import views_html
from . import views_mesa
from . import views_impressao

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
    
    # Views de impressão
    path('<int:pedido_id>/visualizar-comanda/', views_impressao.visualizar_comanda, name='visualizar_comanda'),
    path('<int:pedido_id>/download-comanda/', views_impressao.download_comanda, name='download_comanda'),
    path('<int:pedido_id>/imprimir-comanda/', views_impressao.imprimir_comanda, name='imprimir_comanda'),
    path('testar-impressora/', views_impressao.testar_impressora, name='testar_impressora'),
    path('imprimir-teste/', views_impressao.imprimir_teste, name='imprimir_teste'),
    
    # AJAX endpoints
    path('ajax/buscar-cliente/', views_html.ajax_buscar_cliente, name='ajax_buscar_cliente'),
    path('ajax/buscar-produtos/', views_html.ajax_buscar_produtos, name='ajax_buscar_produtos'),
    path('ajax/calcular-taxa-entrega/', views_html.ajax_calcular_taxa_entrega, name='ajax_calcular_taxa_entrega'),
    path('ajax/cliente/<int:cliente_id>/enderecos/', views_html.ajax_cliente_enderecos, name='ajax_cliente_enderecos'),
    
    # API do pedido rápido
    path('api/criar-rapido/', views_html.api_criar_pedido_rapido, name='api_criar_pedido_rapido'),
    
    # URLs de Mesas
    path('mesas/', views_mesa.listar_mesas, name='listar_mesas'),
    path('mesas/abrir/', views_mesa.abrir_mesa, name='abrir_mesa'),
    path('mesas/<int:mesa_id>/', views_mesa.detalhes_mesa, name='detalhes_mesa'),
    path('mesas/<int:mesa_id>/adicionar-pedido/', views_mesa.adicionar_pedido_mesa, name='adicionar_pedido_mesa'),
    path('mesas/<int:mesa_id>/fechar/', views_mesa.fechar_mesa, name='fechar_mesa'),
    path('mesas/<int:mesa_id>/imprimir-comanda/', views_mesa.imprimir_comanda_mesa, name='imprimir_comanda_mesa'),
    path('mesas/<int:mesa_id>/api/status/', views_mesa.api_status_mesa, name='api_status_mesa'),
    
    # Configurações
    path('configuracao/senha-cancelamento/', views_html.configuracao_senha_cancelamento, name='configuracao_senha_cancelamento'),
]