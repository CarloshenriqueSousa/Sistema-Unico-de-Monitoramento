# professores/views.py
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from core.permissions import IsProfessor, IsPDT, IsEscola
from .models import Professor, PDT
from .serializers import ProfessorSerializer, PDTSerializer
from placement.models import MapeamentoSala
from placement.serializers import MapeamentoSerializer
from atividades.models import Atividade
from atividades.serializers import AtividadeSerializer
from placement.ia import gerar_atividade

class ProfessorViewSet(viewsets.ModelViewSet):
    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer
    permission_classes = [IsAuthenticated, IsProfessor | IsPDT]

    def get_queryset(self):
        return Professor.objects.filter(usuario=self.request.user)

    def perform_update(self, serializer):
        serializer.save()

class PDTViewSet(viewsets.ModelViewSet):
    queryset = PDT.objects.all()
    serializer_class = PDTSerializer
    permission_classes = [IsAuthenticated, IsPDT]

    def get_queryset(self):
        return PDT.objects.filter(usuario=self.request.user)

class DashboardProfessorAPIView(APIView):
    permission_classes = [IsAuthenticated, IsProfessor | IsPDT]

    def get(self, request):
        if request.user.user_type == 'professor':
            try:
                professor = Professor.objects.get(usuario=request.user)
                turmas = professor.turmas.all()
            except Professor.DoesNotExist:
                # Tenta como PDT
                pdt = PDT.objects.get(usuario=request.user)
                turmas = [pdt.turma]
        else:
            # Assumindo que é PDT ou outro tipo de professor
            try:
                pdt = PDT.objects.get(usuario=request.user)
                turmas = [pdt.turma]
            except PDT.DoesNotExist:
                # Tenta como Professor normal
                professor = Professor.objects.get(usuario=request.user)
                turmas = professor.turmas.all()
        data = {
            'turmas': [turma.nome for turma in turmas],
        }
        return Response(data)

class EditarMapeamentoAPIView(APIView):
    permission_classes = [IsAuthenticated, IsProfessor | IsPDT]

    def get(self, request, turma_id):
        mapeamentos = MapeamentoSala.objects.filter(sala_id=turma_id)
        serializer = MapeamentoSerializer(mapeamentos, many=True)
        return Response(serializer.data)

    def post(self, request, turma_id):
        data = request.data
        for item in data:
            mapeamento = MapeamentoSala.objects.get(id=item['id'])
            mapeamento.posicao_x = item['posicao_x']
            mapeamento.posicao_y = item['posicao_y']
            mapeamento.grupo = item.get('grupo', 0)
            mapeamento.save()
        return Response({'message': 'Mapeamento atualizado'})

class CriarAtividadeAPIView(APIView):
    permission_classes = [IsAuthenticated, IsProfessor | IsPDT]

    def post(self, request):
        descricao = request.data['descricao']
        tipo = request.data['tipo']
        turma_id = request.data['turma_id']
        conteudo_ia = gerar_atividade(descricao, tipo)
        data = request.data.copy()
        data['descricao'] += conteudo_ia
        data['gerada_por_ia'] = True
        data['sala'] = turma_id
        data['professor'] = request.user.id
        serializer = AtividadeSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)