import logging

logger = logging.getLogger(__name__)

class DebugMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Log da requisição
        if 'meio-a-meio' in request.path:
            print(f"🔍 DEBUG MIDDLEWARE:")
            print(f"  Method: {request.method}")
            print(f"  Path: {request.path}")
            print(f"  Full URL: {request.build_absolute_uri()}")
            print(f"  Headers: {dict(request.headers)}")
            if hasattr(request, 'data'):
                print(f"  Data: {request.data}")
            print(f"  GET params: {request.GET}")
            print(f"  POST params: {request.POST}")

        response = self.get_response(request)

        # Log da resposta
        if 'meio-a-meio' in request.path:
            print(f"  Response Status: {response.status_code}")
            if hasattr(response, 'data'):
                print(f"  Response Data: {response.data}")

        return response