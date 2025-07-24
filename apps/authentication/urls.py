from django.urls import path
from django.shortcuts import redirect

app_name = 'authentication'

# URLs dummy - sistema sem autenticação
def dummy_view(request):
    return redirect('home')

urlpatterns = [
    path('login/', dummy_view, name='login'),
    path('logout/', dummy_view, name='logout'),
    path('register/', dummy_view, name='register'),
]
