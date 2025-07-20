from django.urls import path
from . import views_html

app_name = 'clientes'

urlpatterns = [
    # Clientes
    path('', views_html.ClienteListView.as_view(), name='cliente-list'),
    path('novo/', views_html.ClienteCreateView.as_view(), name='cliente-create'),
    path('<int:pk>/', views_html.ClienteDetailView.as_view(), name='cliente-detail'),
    path('<int:pk>/editar/', views_html.ClienteUpdateView.as_view(), name='cliente-update'),
    path('<int:pk>/excluir/', views_html.ClienteDeleteView.as_view(), name='cliente-delete'),
    
    # Endereços
    path('<int:cliente_pk>/endereco/novo/', views_html.EnderecoCreateView.as_view(), name='endereco-create'),
    path('endereco/<int:pk>/editar/', views_html.EnderecoUpdateView.as_view(), name='endereco-update'),
    path('endereco/<int:pk>/excluir/', views_html.EnderecoDeleteView.as_view(), name='endereco-delete'),
]