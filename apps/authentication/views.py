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
                    
                    # Login no Django
                    django_login(request, user, backend='authentication.backends.SupabaseBackend')
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
        
        try:
            supabase = get_supabase_client()
            
            # Login no Supabase
            print(f"DEBUG: Tentando login no Supabase com {email}")
            response = supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            print(f"DEBUG: Response do Supabase = {type(response).__name__}")
            
            if response.user:
                # Busca ou cria usuário Django
                user, created = User.objects.get_or_create(
                    username=email,
                    defaults={'email': email}
                )
                
                # Armazena tokens na sessão
                request.session['supabase_access_token'] = response.session.access_token
                request.session['supabase_refresh_token'] = response.session.refresh_token
                
                # Login no Django
                django_login(request, user, backend='authentication.backends.SupabaseBackend')
                
                print(f"DEBUG LOGIN: Usuário {user.username} logado com sucesso")
                print(f"DEBUG LOGIN: request.user = {request.user}, authenticated = {request.user.is_authenticated}")
                
                messages.success(request, "Login realizado com sucesso!")
                return redirect('home')
                
        except AuthApiError as e:
            print(f"DEBUG: AuthApiError - {e}")
            messages.error(request, "Email ou senha inválidos.")
        except Exception as e:
            print(f"DEBUG: Erro inesperado: {e}")
            import traceback
            traceback.print_exc()
            messages.error(request, "Erro ao fazer login.")
    
    return render(request, 'authentication/login.html')

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
