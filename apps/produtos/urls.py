from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'categorias', views.CategoriaViewSet)
router.register(r'tamanhos', views.TamanhoViewSet)
router.register(r'produtos', views.ProdutoViewSet)
router.register(r'precos', views.ProdutoPrecoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]