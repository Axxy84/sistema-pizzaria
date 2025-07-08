from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'caixas', views.CaixaViewSet)
router.register(r'movimentos', views.MovimentoCaixaViewSet)
router.register(r'contas-pagar', views.ContaPagarViewSet)

urlpatterns = [
    path('', include(router.urls)),
]