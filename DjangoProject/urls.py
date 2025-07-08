"""
URL configuration for DjangoProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('force-login/', views.force_login_view, name='force_login'),
    path('api/dashboard-data/', views.dashboard_data_api, name='dashboard_data_api'),
    path('admin/', admin.site.urls),
    path('auth/', include('apps.authentication.urls')),
    path('api/auth/', include('apps.authentication.api_urls')),
    path('api/produtos/', include('apps.produtos.urls')),
    path('api/clientes/', include('apps.clientes.urls')),
    path('api/pedidos/', include('apps.pedidos.urls')),
    path('api/estoque/', include('apps.estoque.urls')),
    path('api/financeiro/', include('apps.financeiro.urls')),
    path('api/dashboard/', include('apps.dashboard.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
