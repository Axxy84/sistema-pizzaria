from django.urls import path
from . import views

app_name = 'settings'

urlpatterns = [
    # API para preferências do usuário
    path('api/user/preferences/', views.user_preferences_api, name='user_preferences_api'),
    
    # APIs específicas para tema
    path('api/user/theme/', views.get_theme_preference, name='get_theme_preference'),
    path('api/user/theme/set/', views.set_theme_preference, name='set_theme_preference'),
    
    # API pública para tema inicial
    path('api/theme/initial/', views.get_initial_theme, name='get_initial_theme'),
]