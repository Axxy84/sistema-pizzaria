from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth import logout
from services.supabase_client import get_supabase_client
from gotrue.errors import AuthApiError

class SupabaseSessionMiddleware(MiddlewareMixin):
    """
    Middleware para validar sessões do Supabase - SIMPLIFICADO
    """
    
    def process_request(self, request):
        # Middleware desativado temporariamente para debug
        # Remove verificações que podem causar loops
        
        # Apenas adiciona o token do Supabase no request se existir
        access_token = request.session.get('supabase_access_token')
        if access_token:
            request.supabase_access_token = access_token
        
        return None