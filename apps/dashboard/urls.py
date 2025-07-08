from django.urls import path
from . import views

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('vendas-periodo/', views.VendasPeriodoView.as_view(), name='vendas-periodo'),
    path('produtos-ranking/', views.ProdutosRankingView.as_view(), name='produtos-ranking'),
]