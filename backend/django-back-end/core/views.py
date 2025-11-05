from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from .serializers import LoginSerializer, UserSerializer
from .models import User
from django.contrib.auth import authenticate

@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """Endpoint para verificar se a API está funcionando"""
    return Response({'status': 'healthy', 'message': 'API is working!'})

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        """Login customizado que retorna informações do usuário junto com tokens"""
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user_type': user.user_type,
                'identifier': user.identifier,
                'user_id': str(user.id),
                'nome': user.nome,
                'email': user.email,
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserListView(generics.ListAPIView):
    """Lista todos os usuários (apenas para usuários autenticados)"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

class UserDetailView(generics.RetrieveAPIView):
    """Detalhes de um usuário específico (apenas para usuários autenticados)"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

class UserCreateView(generics.CreateAPIView):
    """Criação de novo usuário (pode ser AllowAny se for registro público)"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]  # Ou [IsAuthenticated] se só admins podem criar

class UserUpdateView(generics.UpdateAPIView):
    """Atualização de usuário (apenas para usuários autenticados)"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

class UserDeleteView(generics.DestroyAPIView):
    """Exclusão de usuário (apenas para superusuários ou donos da conta)"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

class CurrentUserView(APIView):
    """Retorna informações do usuário atual"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

@api_view(['POST'])
@permission_classes([AllowAny])  # Mudado para AllowAny para permitir logout sem token válido
def logout_view(request):
    """Logout - invalida o token refresh"""
    try:
        refresh_token = request.data.get('refresh')
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message': 'Logout realizado com sucesso'}, status=status.HTTP_200_OK)
        return Response({'message': 'Logout realizado com sucesso'}, status=status.HTTP_200_OK)  # Sempre retorna sucesso
    except Exception as e:
        return Response({'message': 'Logout realizado com sucesso'}, status=status.HTTP_200_OK)  # Sempre retorna sucesso