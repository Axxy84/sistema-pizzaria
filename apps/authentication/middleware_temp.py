"""
Middleware temporário para bypass de autenticação
ATENÇÃO: Remover em produção!
"""

from django.contrib.auth.models import AnonymousUser
from django.utils.deprecation import MiddlewareMixin


class TemporaryUser:
    """Usuário temporário para desenvolvimento sem autenticação"""
    
    def __init__(self):
        self.id = 999999
        self.pk = 999999
        self.username = 'temp_user'
        self.email = 'temp@pizzaria.com'
        self.first_name = 'Usuário'
        self.last_name = 'Temporário'
        self.is_active = True
        self.is_staff = True
        self.is_superuser = True
        self.is_authenticated = True
        self.is_anonymous = False
        
    def __str__(self):
        return self.username
    
    def has_perm(self, perm, obj=None):
        return True
    
    def has_perms(self, perm_list, obj=None):
        return True
    
    def has_module_perms(self, module):
        return True
    
    def get_username(self):
        return self.username


class BypassAuthMiddleware(MiddlewareMixin):
    """
    Middleware que força todos os requests a terem um usuário autenticado
    APENAS PARA DESENVOLVIMENTO - NÃO USAR EM PRODUÇÃO!
    """
    
    def process_request(self, request):
        # Se não há usuário ou é anônimo, criar um temporário
        if not hasattr(request, 'user') or not request.user.is_authenticated:
            request.user = TemporaryUser()
            print("🔓 BYPASS AUTH: Usando usuário temporário (DESENVOLVIMENTO APENAS!)")
        
        return None