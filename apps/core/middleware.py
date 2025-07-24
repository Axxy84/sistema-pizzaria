"""
Middleware para sistema sem autenticação
"""
from django.contrib.auth.models import AnonymousUser

class FakeUser:
    """Usuário falso para sistema sem autenticação"""
    id = 1
    pk = 1
    username = 'sistema'
    first_name = 'Sistema'
    last_name = 'Pizzaria'
    email = 'sistema@pizzaria.com'
    is_staff = True
    is_active = True
    is_superuser = False
    is_authenticated = True
    is_anonymous = False
    
    def __str__(self):
        return self.username
    
    def get_username(self):
        return self.username
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_short_name(self):
        return self.first_name
    
    def has_perm(self, perm):
        return True
    
    def has_perms(self, perms):
        return True
    
    def has_module_perms(self, module):
        return True


class NoAuthMiddleware:
    """Middleware que adiciona usuário falso a todas as requisições"""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Sempre usar o usuário falso
        request.user = FakeUser()
        
        response = self.get_response(request)
        
        return response