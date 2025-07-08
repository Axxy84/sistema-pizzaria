from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth import logout
from services.supabase_client import get_supabase_client
from gotrue.errors import AuthApiError

class SupabaseSessionMiddleware(MiddlewareMixin):
    """
    Middleware para validar sessões do Supabase
    """
    
    def process_request(self, request):
        # Verifica se há token de acesso na sessão
        access_token = request.session.get('supabase_access_token')
        
        if access_token and request.user.is_authenticated:
            try:
                supabase = get_supabase_client()
                
                # Verifica se o token ainda é válido
                response = supabase.auth.get_user(access_token)
                
                if not response.user:
                    # Token inválido, faz logout
                    logout(request)
                    if 'supabase_access_token' in request.session:
                        del request.session['supabase_access_token']
                    if 'supabase_refresh_token' in request.session:
                        del request.session['supabase_refresh_token']
                else:
                    # Atualiza informações do usuário se necessário
                    request.supabase_user = response.user
                    
            except AuthApiError:
                # Token expirado ou inválido
                refresh_token = request.session.get('supabase_refresh_token')
                
                if refresh_token:
                    try:
                        # Tenta renovar o token
                        response = supabase.auth.refresh_session(refresh_token)
                        if response.session:
                            request.session['supabase_access_token'] = response.session.access_token
                            request.session['supabase_refresh_token'] = response.session.refresh_token
                            request.supabase_user = response.user
                        else:
                            logout(request)
                    except:
                        logout(request)
                else:
                    logout(request)
            except Exception:
                # Qualquer outro erro, mantém o usuário logado mas sem validação Supabase
                pass
        
        return None