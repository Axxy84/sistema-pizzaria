"""
Middleware de debug para rastrear problemas de autenticação
"""
from django.utils.deprecation import MiddlewareMixin

class AuthenticationDebugMiddleware(MiddlewareMixin):
    """
    Middleware para debug de autenticação
    """
    
    def process_request(self, request):
        """Log no início da requisição"""
        print(f"\n=== DEBUG MIDDLEWARE - REQUEST ===")
        print(f"Path: {request.path}")
        print(f"Method: {request.method}")
        print(f"Session Key (antes): {request.session.session_key}")
        print(f"User (antes): {request.user}")
        print(f"Is Authenticated (antes): {request.user.is_authenticated if hasattr(request, 'user') else 'No user yet'}")
        
        # Log cookies
        sessionid = request.COOKIES.get('pizzaria_sessionid', 'NOT FOUND')
        print(f"Session Cookie: {sessionid[:10]}..." if sessionid != 'NOT FOUND' else "Session Cookie: NOT FOUND")
        
        return None
    
    def process_response(self, request, response):
        """Log no final da requisição"""
        print(f"\n=== DEBUG MIDDLEWARE - RESPONSE ===")
        print(f"Path: {request.path}")
        print(f"Status: {response.status_code}")
        print(f"Session Key (depois): {request.session.session_key if hasattr(request, 'session') else 'No session'}")
        print(f"User (depois): {request.user if hasattr(request, 'user') else 'No user'}")
        print(f"Is Authenticated (depois): {request.user.is_authenticated if hasattr(request, 'user') else 'No user'}")
        
        # Verifica se a sessão foi modificada
        if hasattr(request, 'session') and hasattr(request.session, 'modified'):
            print(f"Session Modified: {request.session.modified}")
            
        # Verifica cookies de resposta
        if 'Set-Cookie' in response:
            print(f"Setting cookies: Yes")
        
        print("=" * 40)
        
        return response