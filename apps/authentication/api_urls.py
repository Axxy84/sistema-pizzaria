from django.urls import path
from rest_framework.routers import DefaultRouter
from . import api_views

router = DefaultRouter()

urlpatterns = [
    path('register/', api_views.RegisterView.as_view(), name='api-register'),
    path('login/', api_views.LoginView.as_view(), name='api-login'),
    path('logout/', api_views.LogoutView.as_view(), name='api-logout'),
    path('user/', api_views.UserDetailView.as_view(), name='api-user'),
    path('change-password/', api_views.ChangePasswordView.as_view(), name='api-change-password'),
] + router.urls