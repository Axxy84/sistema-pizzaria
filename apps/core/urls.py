"""
URLs para monitoramento de cache (apenas em DEBUG)
"""
from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('cache/status/', views.cache_status, name='cache_status'),
    path('cache/clear/', views.clear_cache, name='clear_cache'),
    path('cache/test/', views.cache_test, name='cache_test'),
]