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
        
        try:
            supabase = get_supabase_client()
            
            # Tenta fazer login no Supabase
            response = supabase.auth.sign_in_with_password({
                "email": username,
                "password": password
            })
            
            if response.user:
                # Cria ou atualiza o usuário Django
                user, created = User.objects.get_or_create(
                    username=username,
                    defaults={
                        'email': username,
                        'first_name': response.user.user_metadata.get('first_name', ''),
                        'last_name': response.user.user_metadata.get('last_name', ''),
                    }
                )
                
                # Armazena o token de sessão do Supabase
                if hasattr(request, 'session'):
                    request.session['supabase_access_token'] = response.session.access_token
                    request.session['supabase_refresh_token'] = response.session.refresh_token
                
                return user
                
        except AuthApiError:
            return None
        except Exception:
            return None
        
        return None
    
    def get_user(self, user_id):
        try:
            user = User.objects.get(pk=user_id)
            print(f"DEBUG BACKEND: get_user chamado para ID {user_id}, encontrou: {user.username}")
            return user
        except User.DoesNotExist:
            print(f"DEBUG BACKEND: get_user chamado para ID {user_id}, usuário não encontrado")
            return None