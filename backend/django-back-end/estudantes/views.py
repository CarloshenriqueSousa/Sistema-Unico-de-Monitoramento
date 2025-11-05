# estudantes/views.py
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from core.permissions import IsAluno, IsProfessor, IsEscola, IsPDT
from .models import Estudante, Nota, Falta
from .serializers import EstudanteSerializer, NotaSerializer, FaltaSerializer
from placement.models import MapeamentoSala
from placement.serializers import MapeamentoSerializer
from atividades.models import Atividade
from atividades.serializers import AtividadeSerializer

class EstudanteViewSet(viewsets.ModelViewSet):
    queryset = Estudante.objects.all()
    serializer_class = EstudanteSerializer
    permission_classes = [IsAuthenticated, IsAluno | IsProfessor | IsEscola | IsPDT]

    def get_queryset(self):
        if self.request.user.user_type == 'aluno':
            return Estudante.objects.filter(usuario=self.request.user)
        return super().get_queryset()

    def perform_update(self, serializer):
        serializer.save()

class NotaViewSet(viewsets.ModelViewSet):
    queryset = Nota.objects.all()
    serializer_class = NotaSerializer
    permission_classes = [IsAuthenticated, IsAluno | IsProfessor | IsEscola | IsPDT]

    def get_queryset(self):
        if self.request.user.user_type == 'aluno':
            estudante = Estudante.objects.get(usuario=self.request.user)
            return Nota.objects.filter(estudante=estudante)
        return super().get_queryset()

class FaltaViewSet(viewsets.ModelViewSet):
    queryset = Falta.objects.all()
    serializer_class = FaltaSerializer
    permission_classes = [IsAuthenticated, IsAluno | IsProfessor | IsEscola | IsPDT]

    def get_queryset(self):
        if self.request.user.user_type == 'aluno':
            estudante = Estudante.objects.get(usuario=self.request.user)
            return Falta.objects.filter(estudante=estudante)
        return super().get_queryset()

class DashboardAlunoAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAluno]

    def get(self, request):
        estudante = Estudante.objects.get(usuario=request.user)
        notas = Nota.objects.filter(estudante=estudante)
        faltas = Falta.objects.filter(estudante=estudante)
        mapeamento = MapeamentoSala.objects.filter(estudante=estudante).first()
        atividades = Atividade.objects.filter(sala=estudante.turma)
        data = {
            'estudante': EstudanteSerializer(estudante).data,
            'notas': NotaSerializer(notas, many=True).data,
            'faltas': FaltaSerializer(faltas, many=True).data,
            'mapeamento': MapeamentoSerializer(mapeamento).data if mapeamento else None,
            'atividades': AtividadeSerializer(atividades, many=True).data,
        }
        return Response(data)

class LeaderboardAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        estudantes = Estudante.objects.order_by('-dots_pontos')[:10]
        serializer = EstudanteSerializer(estudantes, many=True)
        return Response(serializer.data)