from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

@require_http_methods(["GET"])
def session_info_view(request):
    """View para debug - mostra informações da sessão atual"""
    session_data = {
        'user': {
            'is_authenticated': request.user.is_authenticated,
            'id': request.user.id if request.user.is_authenticated else None,
            'username': request.user.username if request.user.is_authenticated else None,
            'email': request.user.email if request.user.is_authenticated else None,
        },
        'session': {
            'session_key': request.session.session_key,
            '_auth_user_id': request.session.get('_auth_user_id'),
            '_auth_user_backend': request.session.get('_auth_user_backend'),
            '_auth_user_hash': request.session.get('_auth_user_hash'),
            'supabase_access_token': bool(request.session.get('supabase_access_token')),
            'supabase_refresh_token': bool(request.session.get('supabase_refresh_token')),
            'supabase_user_id': request.session.get('supabase_user_id'),
        },
        'cookies': {
            'sessionid': request.COOKIES.get('pizzaria_sessionid', 'Not found'),
            'csrftoken': bool(request.COOKIES.get('csrftoken')),
        },
        'meta': {
            'HTTP_COOKIE': bool(request.META.get('HTTP_COOKIE')),
            'REMOTE_ADDR': request.META.get('REMOTE_ADDR'),
        }
    }
    
    return JsonResponse(session_data, json_dumps_params={'indent': 2})

@login_required
def protected_view(request):
    """View protegida para testar autenticação"""
    return JsonResponse({
        'message': 'Você está autenticado!',
        'user': request.user.username,
        'user_id': request.user.id,
    })