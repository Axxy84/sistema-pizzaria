from django.urls import path
from . import views

app_name = 'financeiro'

# Template-based routes for cash closing system  
urlpatterns = [
    path('', views.CaixaDashboardView.as_view(), name='dashboard'),
    path('abrir-caixa/', views.AbrirCaixaView.as_view(), name='abrir_caixa'),
    path('fechar-caixa/', views.FecharCaixaView.as_view(), name='fechar_caixa'),
    path('adicionar-movimento/', views.AdicionarMovimentoView.as_view(), name='adicionar_movimento'),
    path('historico/', views.HistoricoCaixaView.as_view(), name='historico'),
    path('caixa/<int:pk>/', views.DetalhesCaixaView.as_view(), name='detalhes_caixa'),
]