from django.urls import path
from . import views, views_html

urlpatterns = [
    # API endpoints
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('vendas-periodo/', views.VendasPeriodoView.as_view(), name='vendas-periodo'),
    path('produtos-ranking/', views.ProdutosRankingView.as_view(), name='produtos-ranking'),
    
    # HTML view
    path('html/', views_html.dashboard_view, name='dashboard_html'),
]
