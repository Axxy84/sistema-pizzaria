from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'unidades', views.UnidadeMedidaViewSet)
router.register(r'ingredientes', views.IngredienteViewSet)
router.register(r'movimentos', views.MovimentoEstoqueViewSet)
router.register(r'receitas', views.ReceitaProdutoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]