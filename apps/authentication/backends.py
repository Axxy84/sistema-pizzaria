from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from services.supabase_client import get_supabase_client
from gotrue.errors import AuthApiError

class SupabaseBackend(BaseBackend):
    """
    Backend de autenticação customizado que usa Supabase Auth
    """
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None or password is None:
            return None
        
        # Tenta com Supabase primeiro
        try:
            supabase = get_supabase_client()
            
            # Tenta fazer login no Supabase
            response = supabase.auth.sign_in_with_password({
                "email": username,
                "password": password
            })
            
            if response.user:
                # Cria um usuário Django temporário na memória
                # Não salvamos no banco para evitar problemas de conexão
                user = User(
                    id=999999,  # ID temporário
                    username=username,
                    email=username,
                    first_name=response.user.user_metadata.get('first_name', 'Admin'),
                    last_name=response.user.user_metadata.get('last_name', 'Pizzaria'),
                    is_active=True,
                    is_staff=True,
                    is_superuser=True
                )
                
                # Marca como um usuário Supabase para referência
                user._supabase_user_id = response.user.id
                user._state.adding = False  # Indica que não é um novo objeto
                
                # Armazena o token de sessão do Supabase
                if hasattr(request, 'session'):
                    request.session['supabase_access_token'] = response.session.access_token
                    request.session['supabase_refresh_token'] = response.session.refresh_token
                    request.session['supabase_user_id'] = response.user.id
                    request.session['user_email'] = username
                
                print(f"DEBUG BACKEND: Autenticação Supabase bem-sucedida para {username}")
                return user
                
        except AuthApiError as e:
            print(f"DEBUG BACKEND: Erro Supabase - {e}")
            return None
        except Exception as e:
            print(f"DEBUG BACKEND: Erro inesperado - {e}")
            return None
        
        return None
    
    def get_user(self, user_id):
        # Para usuários Supabase, retornamos um objeto temporário
        if user_id == 999999:
            # Cria um usuário temporário baseado na sessão
            user = User(
                id=999999,
                username='admin@pizzaria.com',  # Usar email padrão
                email='admin@pizzaria.com',
                first_name='Admin',
                last_name='Pizzaria',
                is_active=True,
                is_staff=True,
                is_superuser=True
            )
            user._state.adding = False
            print(f"DEBUG BACKEND: get_user retornando usuário temporário")
            return user
        
        return None