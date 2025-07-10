from django.urls import path
from . import views_html

urlpatterns = [
    # Lista geral de produtos
    path('', views_html.ProductListView.as_view(), name='product_list'),
    
    # Filtros por tipo
    path('pizzas/', views_html.ProductFilterView.as_view(), {'tipo': 'pizza'}, name='pizza_list'),
    path('bebidas/', views_html.ProductFilterView.as_view(), {'tipo': 'bebida'}, name='bebida_list'),
    path('bordas/', views_html.ProductFilterView.as_view(), {'tipo': 'borda'}, name='borda_list'),
    path('sobremesas/', views_html.ProductFilterView.as_view(), {'tipo': 'sobremesa'}, name='sobremesa_list'),
    path('acompanhamentos/', views_html.ProductFilterView.as_view(), {'tipo': 'acompanhamento'}, name='acompanhamento_list'),
    
    # Views específicas para pizzas (estilo cardápio)
    path('pizzas/cardapio/', views_html.PizzaTableView.as_view(), name='pizza_table'),
    path('pizzas/nova/', views_html.PizzaCreateView.as_view(), name='pizza_create'),
    path('pizzas/<int:pk>/editar/', views_html.PizzaUpdateView.as_view(), name='pizza_update'),
    
    # CRUD
    path('novo/', views_html.ProductCreateView.as_view(), name='product_create'),
    path('<int:pk>/editar/', views_html.ProductUpdateView.as_view(), name='product_update'),
    path('<int:pk>/excluir/', views_html.ProductDeleteView.as_view(), name='product_delete'),
    
    # Busca
    path('buscar/', views_html.ProductSearchView.as_view(), name='product_search'),
    
    # AJAX
    path('<int:pk>/toggle/', views_html.product_toggle_status, name='product_toggle_status'),
]