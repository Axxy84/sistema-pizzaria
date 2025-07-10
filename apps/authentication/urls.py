from django.urls import path
from . import views
from . import test_views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('login-django/', views.django_login_view, name='django_login'),  # LOGIN APENAS DJANGO
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    
    # URLs de teste/debug
    path('session-info/', test_views.session_info_view, name='session_info'),
    path('protected/', test_views.protected_view, name='protected_test'),
]