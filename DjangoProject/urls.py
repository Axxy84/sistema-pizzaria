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
from django.shortcuts import redirect
from . import views

# View dummy para URLs de autenticação (sistema sem login)
def dummy_auth(request):
    return redirect('home')

urlpatterns = [
    path('', views.home_view, name='home'),
    path('pizzas-promocionais/', views.pizzas_promocionais_view, name='pizzas_promocionais'),
    path('test-loading/', views.test_loading_view, name='test_loading'),
    path('api/dashboard-data/', views.dashboard_data_api, name='dashboard_data_api'),
    path('admin/', admin.site.urls),
    
    # URLs de autenticação (dummy - sistema sem autenticação)
    path('login/', dummy_auth, name='login'),
    path('logout/', dummy_auth, name='logout'),
    path('register/', dummy_auth, name='register'),
    
    # URLs HTML dos apps
    path('dashboard/', include('apps.dashboard.urls')),
    path('produtos/', include('apps.produtos.urls_html')),
    path('pedidos/', include('apps.pedidos.urls_html')),
    path('financeiro/', include('apps.financeiro.urls')),
    path('clientes/', include('apps.clientes.urls_html')),
    path('estoque/', include('apps.estoque.urls_html')),
    
    # APIs REST
    path('api/produtos/', include('apps.produtos.urls')),
    path('api/clientes/', include('apps.clientes.urls')),
    path('api/pedidos/', include('apps.pedidos.urls')),
    path('api/estoque/', include('apps.estoque.urls')),
    path('api/financeiro/', include('apps.financeiro.api_urls')),
    path('api/dashboard/', include('apps.dashboard.urls')),
    
    # Settings/Preferences API
    path('', include('settings.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
