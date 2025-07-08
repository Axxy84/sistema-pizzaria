from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from services.supabase_client import get_supabase_client
from gotrue.errors import AuthApiError
from .serializers import (
    UserSerializer, RegisterSerializer,
    LoginSerializer, ChangePasswordSerializer
)

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Registra no Supabase também
        try:
            supabase = get_supabase_client()
            response = supabase.auth.sign_up({
                "email": serializer.validated_data['email'],
                "password": serializer.validated_data['password'],
                "options": {
                    "data": {
                        "first_name": serializer.validated_data.get('first_name', ''),
                        "last_name": serializer.validated_data.get('last_name', ''),
                    }
                }
            })
            
            if response.user:
                # Cria usuário Django
                user = serializer.save()
                return Response(
                    UserSerializer(user).data,
                    status=status.HTTP_201_CREATED
                )
            
        except AuthApiError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return Response(
            {'error': 'Erro ao registrar usuário'},
            status=status.HTTP_400_BAD_REQUEST
        )

class LoginView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        
        # Autentica via backend Supabase
        user = authenticate(request, username=email, password=password)
        
        if user:
            login(request, user)
            return Response(UserSerializer(user).data)
        
        return Response(
            {'error': 'Credenciais inválidas'},
            status=status.HTTP_401_UNAUTHORIZED
        )

class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({'message': 'Logout realizado com sucesso'})

class UserDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = request.user
        
        # Verifica senha atual
        if not user.check_password(serializer.validated_data['old_password']):
            return Response(
                {'error': 'Senha atual incorreta'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Atualiza senha no Django
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        
        # Tenta atualizar no Supabase também
        try:
            if 'supabase_access_token' in request.session:
                supabase = get_supabase_client()
                supabase.auth.update_user({
                    'password': serializer.validated_data['new_password']
                })
        except:
            pass  # Se falhar no Supabase, pelo menos atualizou no Django
        
        return Response({'message': 'Senha alterada com sucesso'})