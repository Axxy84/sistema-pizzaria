from django.conf import settings

class CleanLayoutMiddleware:
    """
    Middleware para definir o layout clean como padrão em todo o sistema
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Define layout clean como padrão
        request.use_clean_layout = request.GET.get('layout') != 'classic'
        
        response = self.get_response(request)
        return response