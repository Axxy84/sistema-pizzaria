"""
Middleware para sistema sem autenticação
"""
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.db import connection

User = get_user_model()

class NoAuthMiddleware:
    """Middleware que adiciona usuário do sistema a todas as requisições"""
    
    def __init__(self, get_response):
        self.get_response = get_response
        self._system_user = None
        self._user_id = 1  # ID fixo para o usuário do sistema
    
    def get_system_user(self):
        """Obtém ou cria o usuário do sistema"""
        if self._system_user is None:
            # Tenta pegar do cache primeiro
            cache_key = f'system_user_{self._user_id}'
            self._system_user = cache.get(cache_key)
            
            if self._system_user is None:
                try:
                    # Verifica se estamos conectados ao banco
                    with connection.cursor() as cursor:
                        cursor.execute("SELECT 1")
                    
                    # Tenta buscar usuário existente por ID
                    try:
                        self._system_user = User.objects.get(id=self._user_id)
                    except User.DoesNotExist:
                        # Tenta por username
                        try:
                            self._system_user = User.objects.get(username='sistema')
                        except User.DoesNotExist:
                            # Cria o usuário do sistema se não existir
                            self._system_user = User.objects.create_user(
                                username='sistema',
                                email='sistema@pizzaria.com',
                                first_name='Sistema',
                                last_name='Pizzaria',
                                is_staff=True,
                                is_active=True
                            )
                    
                    # Salva no cache por 1 hora
                    cache.set(cache_key, self._system_user, 3600)
                    
                except Exception as e:
                    # Se falhar ao conectar no banco, usa um usuário mock
                    print(f"Aviso: Não foi possível obter usuário do banco: {e}")
                    return self.get_mock_user()
        
        return self._system_user
    
    def get_mock_user(self):
        """Retorna um usuário mock quando não há conexão com banco"""
        class MockUser:
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
            
            def save(self, *args, **kwargs):
                pass
            
            def delete(self, *args, **kwargs):
                pass
            
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
            
            # Adiciona _meta para compatibilidade com Django
            class _meta:
                model_name = 'user'
                app_label = 'auth'
        
        return MockUser()
    
    def __call__(self, request):
        # Sempre usar o usuário do sistema
        try:
            request.user = self.get_system_user()
        except Exception as e:
            # Em caso de qualquer erro, usa o mock
            print(f"Aviso: Usando usuário mock devido a erro: {e}")
            request.user = self.get_mock_user()
        
        response = self.get_response(request)
        
        return response