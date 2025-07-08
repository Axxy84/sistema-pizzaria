from django.shortcuts import render, redirect
from django.contrib.auth import login as django_login, logout as django_logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect
from services.supabase_client import get_supabase_client
from gotrue.errors import AuthApiError

@csrf_protect
@require_http_methods(["GET", "POST"])
def register_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        
        # Validações básicas
        if not email or not password:
            messages.error(request, "Email e senha são obrigatórios.")
            return render(request, 'authentication/register.html')
            
        if len(password) < 6:
            messages.error(request, "A senha deve ter pelo menos 6 caracteres.")
            return render(request, 'authentication/register.html')
        
        if password != password_confirm:
            messages.error(request, "As senhas não coincidem.")
            return render(request, 'authentication/register.html')
        
        try:
            supabase = get_supabase_client()
            
            # Registra no Supabase
            response = supabase.auth.sign_up({
                "email": email,
                "password": password,
                "options": {
                    "data": {
                        "first_name": first_name,
                        "last_name": last_name,
                    }
                }
            })
            
            print(f"DEBUG: Supabase response - User: {response.user}, Session: {response.session}")
            
            if response.user:
                # Cria usuário Django
                user, created = User.objects.get_or_create(
                    username=email,
                    defaults={
                        'email': email,
                        'first_name': first_name,
                        'last_name': last_name,
                    }
                )
                
                if response.session:
                    messages.success(request, "Registro realizado com sucesso! Você foi automaticamente logado.")
                    # Armazena tokens na sessão
                    request.session['supabase_access_token'] = response.session.access_token
                    request.session['supabase_refresh_token'] = response.session.refresh_token
                    request.session['supabase_user_id'] = response.user.id
                    
                    # Define o backend antes do login
                    user.backend = 'authentication.backends.SupabaseBackend'
                    
                    # Login no Django
                    django_login(request, user)
                    return redirect('home')
                else:
                    messages.success(request, "Registro realizado com sucesso! Verifique seu email para confirmar.")
                    return redirect('login')
            else:
                messages.error(request, "Não foi possível criar a conta. Tente novamente.")
            
        except AuthApiError as e:
            error_msg = str(e)
            if "already registered" in error_msg.lower():
                messages.error(request, "Este email já está registrado. Tente fazer login.")
            elif "invalid email" in error_msg.lower():
                messages.error(request, "Email inválido.")
            else:
                messages.error(request, f"Erro ao registrar: {error_msg}")
        except Exception as e:
            print(f"DEBUG: Erro inesperado: {e}")
            import traceback
            traceback.print_exc()
            messages.error(request, "Erro inesperado ao registrar. Tente novamente.")
    
    return render(request, 'authentication/register.html')

@csrf_protect
@require_http_methods(["GET", "POST"])
def login_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        print(f"DEBUG LOGIN ATTEMPT: Email={email}, Password={'*' * len(password)}")
        
        # Usar o sistema de autenticação do Django
        from django.contrib.auth import authenticate
        
        print(f"DEBUG: Tentando autenticar com Django/Supabase backend")
        user = authenticate(request, username=email, password=password)
        
        if user:
            # Login no Django
            django_login(request, user)
            
            print(f"DEBUG LOGIN: Usuário {user.username} logado com sucesso")
            print(f"DEBUG LOGIN: request.user = {request.user}, authenticated = {request.user.is_authenticated}")
            print(f"DEBUG LOGIN: Session key = {request.session.session_key}")
            print(f"DEBUG LOGIN: _auth_user_id = {request.session.get('_auth_user_id')}")
            
            messages.success(request, "Login realizado com sucesso!")
            return redirect('home')
        else:
            print(f"DEBUG: Falha na autenticação para {email}")
            messages.error(request, "Email ou senha inválidos.")
    
    return render(request, 'authentication/login.html')

@csrf_protect
@require_http_methods(["GET", "POST"])
def django_login_view(request):
    """Login usando apenas Django ModelBackend (para teste)"""
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        print(f"DEBUG DJANGO LOGIN: {username}, {password}")
        
        from django.contrib.auth import authenticate
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            django_login(request, user)
            print(f"DEBUG DJANGO LOGIN: Sucesso! {user.username}")
            print(f"DEBUG DJANGO LOGIN: Session = {request.session.session_key}")
            messages.success(request, "Login Django realizado com sucesso!")
            return redirect('home')
        else:
            print(f"DEBUG DJANGO LOGIN: Falhou para {username}")
            messages.error(request, "Credenciais inválidas")
    
    return render(request, 'authentication/django_login.html')

@require_http_methods(["POST"])
def logout_view(request):
    try:
        # Logout do Supabase
        if 'supabase_access_token' in request.session:
            supabase = get_supabase_client()
            supabase.auth.sign_out()
            
            # Remove tokens da sessão
            del request.session['supabase_access_token']
            if 'supabase_refresh_token' in request.session:
                del request.session['supabase_refresh_token']
        
        # Logout do Django
        django_logout(request)
        messages.success(request, "Logout realizado com sucesso!")
        
    except Exception as e:
        messages.error(request, "Erro ao fazer logout.")
    
    return redirect('login')
