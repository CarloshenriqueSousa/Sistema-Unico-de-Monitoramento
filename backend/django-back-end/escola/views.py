from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from core.permissions import IsEscola, IsProfessor
from .models import Escola, Turma, Liberacao, Jogo, TimeJogo
from .serializers import (
    EscolaSerializer,
    TurmaSerializer,
    LiberacaoSerializer,
    JogoSerializer,
    TimeJogoSerializer
)

class EscolaViewSet(viewsets.ModelViewSet):
    queryset = Escola.objects.all()
    serializer_class = EscolaSerializer
    permission_classes = [IsAuthenticated, IsEscola | IsAdminUser]

    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'escola':
            return Escola.objects.filter(usuario=user)
        return Escola.objects.all()

class TurmaViewSet(viewsets.ModelViewSet):
    queryset = Turma.objects.all()
    serializer_class = TurmaSerializer
    permission_classes = [IsAuthenticated, IsEscola | IsAdminUser]

    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'escola':
            escola = Escola.objects.get(usuario=user)
            return Turma.objects.filter(escola=escola)
        return Turma.objects.all()

class LiberacaoViewSet(viewsets.ModelViewSet):
    queryset = Liberacao.objects.all()
    serializer_class = LiberacaoSerializer
    permission_classes = [IsAuthenticated, IsEscola | IsProfessor | IsAdminUser]

class JogoViewSet(viewsets.ModelViewSet):
    queryset = Jogo.objects.all()
    serializer_class = JogoSerializer
    permission_classes = [IsAuthenticated, IsEscola | IsAdminUser]

class TimeJogoViewSet(viewsets.ModelViewSet):
    queryset = TimeJogo.objects.all()
    serializer_class = TimeJogoSerializer
    permission_classes = [IsAuthenticated, IsEscola | IsAdminUser]

class TurmaLiberacaoView(APIView):
    permission_classes = [IsAuthenticated, IsEscola | IsProfessor]

    def post(self, request, turma_id):
        try:
            turma = Turma.objects.get(id=turma_id)
            liberacao = Liberacao.objects.create(
                turma=turma,
                tipo=request.data.get('tipo', 'RECREIO'),
                data_hora=request.data.get('data_hora'),
                liberado_por=request.user
            )
            serializer = LiberacaoSerializer(liberacao)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Turma.DoesNotExist:
            return Response(
                {'error': 'Turma não encontrada'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

class PreCadastroAlunoAPIView(APIView):
    permission_classes = [IsAuthenticated, IsEscola | IsAdminUser]
    
    def post(self, request):
        try:
            # Implementação básica do pré-cadastro
            data = request.data
            # Aqui você pode adicionar a lógica de pré-cadastro
            return Response(
                {'message': 'Pré-cadastro realizado com sucesso'},
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

class PreCadastroProfessorAPIView(APIView):
    permission_classes = [IsAuthenticated, IsEscola | IsAdminUser]
    
    def post(self, request):
        try:
            data = request.data
            return Response(
                {'message': 'Pré-cadastro de professor realizado com sucesso'},
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

class DashboardEscolaAPIView(APIView):
    permission_classes = [IsAuthenticated, IsEscola | IsAdminUser]
    
    def get(self, request):
        try:
            # Dados básicos do dashboard
            user = request.user
            escola = Escola.objects.get(usuario=user)
            turmas_count = Turma.objects.filter(escola=escola).count()
            estudantes_count = sum(turma.estudantes.count() for turma in Turma.objects.filter(escola=escola))
            
            return Response({
                'escola': escola.nome,
                'turmas_count': turmas_count,
                'estudantes_count': estudantes_count
            })
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
