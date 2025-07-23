"""
Decoradores temporários para desenvolvimento sem autenticação
"""

from functools import wraps


def login_not_required(view_func):
    """
    Decorador que marca uma view como não requerendo login
    (Na verdade não faz nada pois o middleware já cuida disso)
    """
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        return view_func(request, *args, **kwargs)
    
    wrapped_view.login_not_required = True
    return wrapped_view


# Sobrescrever o login_required do Django temporariamente
def login_required(view_func=None, redirect_field_name='next', login_url=None):
    """
    Versão temporária que não requer login
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(request, *args, **kwargs):
            # Simplesmente executar a view sem verificar autenticação
            return view_func(request, *args, **kwargs)
        return wrapped_view
    
    if view_func:
        return decorator(view_func)
    return decorator