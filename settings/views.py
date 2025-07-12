from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.views import View
import json
from .models import UserPreference

@login_required
@require_http_methods(["GET", "POST"])
def user_preferences_api(request):
    """
    API para gerenciar preferências do usuário
    GET: Retorna as preferências do usuário
    POST: Atualiza as preferências do usuário
    """
    
    if request.method == 'GET':
        # Obter preferências do usuário
        try:
            preference = UserPreference.get_or_create_for_user(request.user)
            return JsonResponse({
                'theme': preference.theme,
                'notifications_enabled': preference.notifications_enabled,
                'language': preference.language,
            })
        except Exception as e:
            return JsonResponse({
                'error': 'Erro ao carregar preferências',
                'message': str(e)
            }, status=500)
    
    elif request.method == 'POST':
        # Atualizar preferências do usuário
        try:
            data = json.loads(request.body)
            preference = UserPreference.get_or_create_for_user(request.user)
            
            # Atualizar campos se fornecidos
            if 'theme' in data:
                if data['theme'] in ['light', 'dark', 'auto']:
                    preference.theme = data['theme']
                else:
                    return JsonResponse({
                        'error': 'Tema inválido',
                        'message': 'Tema deve ser: light, dark ou auto'
                    }, status=400)
            
            if 'notifications_enabled' in data:
                preference.notifications_enabled = bool(data['notifications_enabled'])
            
            if 'language' in data:
                preference.language = data['language']
            
            preference.save()
            
            return JsonResponse({
                'message': 'Preferências atualizadas com sucesso',
                'theme': preference.theme,
                'notifications_enabled': preference.notifications_enabled,
                'language': preference.language,
            })
            
        except json.JSONDecodeError:
            return JsonResponse({
                'error': 'Dados inválidos',
                'message': 'JSON mal formatado'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'error': 'Erro ao salvar preferências',
                'message': str(e)
            }, status=500)


@login_required
def get_theme_preference(request):
    """
    API específica para obter apenas a preferência de tema
    """
    try:
        preference = UserPreference.get_or_create_for_user(request.user)
        return JsonResponse({
            'theme': preference.theme
        })
    except Exception as e:
        return JsonResponse({
            'error': 'Erro ao carregar tema',
            'message': str(e)
        }, status=500)


@login_required
@require_http_methods(["POST"])
def set_theme_preference(request):
    """
    API específica para atualizar apenas a preferência de tema
    """
    try:
        data = json.loads(request.body)
        theme = data.get('theme')
        
        if theme not in ['light', 'dark', 'auto']:
            return JsonResponse({
                'error': 'Tema inválido',
                'message': 'Tema deve ser: light, dark ou auto'
            }, status=400)
        
        preference = UserPreference.get_or_create_for_user(request.user)
        preference.theme = theme
        preference.save()
        
        return JsonResponse({
            'message': 'Tema atualizado com sucesso',
            'theme': preference.theme
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'error': 'Dados inválidos',
            'message': 'JSON mal formatado'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'error': 'Erro ao salvar tema',
            'message': str(e)
        }, status=500)


def get_initial_theme(request):
    """
    API pública para obter o tema inicial (para usuários não logados)
    Retorna 'auto' por padrão
    """
    if request.user.is_authenticated:
        try:
            preference = UserPreference.get_or_create_for_user(request.user)
            return JsonResponse({
                'theme': preference.theme
            })
        except Exception:
            pass
    
    # Fallback para usuários não logados ou erro
    return JsonResponse({
        'theme': 'auto'
    })
