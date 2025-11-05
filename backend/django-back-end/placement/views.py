# placement/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import MapeamentoSala, PosicaoAluno, TemplatesSala
from .serializers import (
    MapeamentoSerializer, 
    PosicaoAlunoSerializer,
    MoverAlunoSerializer,
    AtualizarPosicoesSerializer,
    AtualizarObjetosSerializer,
    TemplatesSalaSerializer
)
from .services import gerar_novo_mapeamento, IAMapeamentoSala
from .permissions import IsProfessorOrPDTOrAdmin
from core.permissions import IsAluno, IsProfessor
from django.shortcuts import get_object_or_404
from escola.models import Turma
from estudantes.models import Estudante

# ==================== DEMONSTRAÇÃO (Público) ====================

class DemoTemplatesView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        """Lista templates públicos para demonstração"""
        templates = TemplatesSala.objects.filter(publico=True).order_by('tipo_sala', 'nome')
        serializer = TemplatesSalaSerializer(templates, many=True)
        return Response(serializer.data)

class DemoTemplateDetailView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, pk):
        """Detalhes de um template específico"""
        template = get_object_or_404(TemplatesSala, pk=pk, publico=True)
        serializer = TemplatesSalaSerializer(template)
        return Response(serializer.data)

# ==================== VISÃO DO ALUNO ====================

class AlunoMapeamentoView(APIView):
    permission_classes = [IsAuthenticated, IsAluno]
    
    def get(self, request):
        """Retorna mapeamento atual do aluno"""
        try:
            estudante = Estudante.objects.get(usuario=request.user)
            turma = estudante.turma
            
            if not turma:
                return Response(
                    {"error": "Aluno não possui turma ativa"},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Busca mapeamento ativo da turma
            mapeamento = MapeamentoSala.objects.filter(
                turma=turma,
                ativo=True
            ).first()
            
            if not mapeamento:
                return Response(
                    {"error": "Turma não possui mapeamento ativo"},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Busca todas as posições
            posicoes = PosicaoAluno.objects.filter(
                mapeamento=mapeamento
            ).select_related('estudante', 'estudante__usuario')
            
            # Busca posição do aluno
            sua_posicao = posicoes.filter(estudante=estudante).first()
            
            return Response({
                "mapeamento": MapeamentoSerializer(mapeamento).data,
                "posicoes": PosicaoAlunoSerializer(posicoes, many=True).data,
                "sua_posicao": PosicaoAlunoSerializer(sua_posicao).data if sua_posicao else None,
                "seu_id": estudante.id
            })
        except Estudante.DoesNotExist:
            return Response(
                {"error": "Usuário não é um estudante"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

# ==================== EDITOR DO PROFESSOR ====================

class ProfessorMapeamentosListView(APIView):
    permission_classes = [IsAuthenticated, IsProfessor]
    
    def get(self, request):
        """Lista mapeamentos do professor"""
        from professores.models import Professor
        
        try:
            professor = Professor.objects.get(usuario=request.user)
            turma_id = request.query_params.get('turma_id')
            
            if turma_id:
                turma = get_object_or_404(Turma, id=turma_id)
                # Valida que o professor tem acesso à turma
                if not professor.turmas.filter(id=turma_id).exists():
                    return Response(
                        {"error": "Professor não tem acesso a esta turma"},
                        status=status.HTTP_403_FORBIDDEN
                    )
                mapeamentos = MapeamentoSala.objects.filter(turma=turma)
            else:
                # Lista mapeamentos de todas as turmas do professor
                turmas_professor = professor.turmas.all()
                mapeamentos = MapeamentoSala.objects.filter(turma__in=turmas_professor)
            
            serializer = MapeamentoSerializer(mapeamentos, many=True)
            return Response(serializer.data)
        except Professor.DoesNotExist:
            return Response(
                {"error": "Usuário não é um professor"},
                status=status.HTTP_404_NOT_FOUND
            )

class ProfessorMapeamentoCreateView(APIView):
    permission_classes = [IsAuthenticated, IsProfessor]
    
    def post(self, request):
        """Cria novo mapeamento"""
        from professores.models import Professor
        
        try:
            professor = Professor.objects.get(usuario=request.user)
            turma_id = request.data.get('turma_id')
            
            if not turma_id:
                return Response(
                    {"error": "turma_id é obrigatório"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            turma = get_object_or_404(Turma, id=turma_id)
            
            # Valida que o professor tem acesso à turma
            if not professor.turmas.filter(id=turma_id).exists():
                return Response(
                    {"error": "Professor não tem acesso a esta turma"},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            # Desativa mapeamentos anteriores da turma
            MapeamentoSala.objects.filter(turma=turma).update(ativo=False)
            
            # Cria novo mapeamento
            serializer = MapeamentoSerializer(data=request.data)
            if serializer.is_valid():
                mapeamento = serializer.save(
                    turma=turma,
                    escola=turma.escola,
                    ativo=True
                )
                return Response(
                    MapeamentoSerializer(mapeamento).data,
                    status=status.HTTP_201_CREATED
                )
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Professor.DoesNotExist:
            return Response(
                {"error": "Usuário não é um professor"},
                status=status.HTTP_404_NOT_FOUND
            )

class ProfessorMapeamentoDetailView(APIView):
    permission_classes = [IsAuthenticated, IsProfessor]
    
    def get(self, request, uuid):
        """Detalhes do mapeamento"""
        mapeamento = get_object_or_404(MapeamentoSala, uuid=uuid)
        
        posicoes = PosicaoAluno.objects.filter(
            mapeamento=mapeamento
        ).select_related('estudante', 'estudante__usuario')
        
        return Response({
            "mapeamento": MapeamentoSerializer(mapeamento).data,
            "posicoes": PosicaoAlunoSerializer(posicoes, many=True).data
        })
    
    def patch(self, request, uuid):
        """Atualiza mapeamento"""
        mapeamento = get_object_or_404(MapeamentoSala, uuid=uuid)
        
        serializer = MapeamentoSerializer(
            mapeamento,
            data=request.data,
            partial=True
        )
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, uuid):
        """Deleta mapeamento"""
        mapeamento = get_object_or_404(MapeamentoSala, uuid=uuid)
        mapeamento.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ProfessorPosicionarAlunosView(APIView):
    permission_classes = [IsAuthenticated, IsProfessor]
    
    def patch(self, request, uuid):
        """Atualiza posições dos alunos (drag-and-drop)"""
        mapeamento = get_object_or_404(MapeamentoSala, uuid=uuid)
        
        serializer = AtualizarPosicoesSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        posicoes_data = serializer.validated_data['posicoes']
        
        # Remove posições antigas
        PosicaoAluno.objects.filter(mapeamento=mapeamento).delete()
        
        # Cria novas posições
        posicoes_criadas = []
        for pos_data in posicoes_data:
            estudante_id = pos_data.get('estudante_id')
            if not estudante_id:
                continue
            
            estudante = get_object_or_404(Estudante, id=estudante_id)
            
            # Calcula grupo se não fornecido
            numero_grupo = pos_data.get('numero_grupo')
            if numero_grupo is None:
                # Calcula grupo baseado na posição
                linha = pos_data.get('linha', 0)
                coluna = pos_data.get('coluna', 0)
                alunos_por_grupo = mapeamento.alunos_por_grupo or 1
                
                if alunos_por_grupo > 1:
                    # Calcula grupo baseado na posição
                    assentos_por_linha = mapeamento.fileiras_horizontais or mapeamento.colunas or 6
                    assento_index = linha * assentos_por_linha + coluna
                    numero_grupo = assento_index // alunos_por_grupo
                    posicao_no_grupo = assento_index % alunos_por_grupo
                else:
                    numero_grupo = None
                    posicao_no_grupo = 0
            
            posicao = PosicaoAluno.objects.create(
                mapeamento=mapeamento,
                estudante=estudante,
                linha=pos_data.get('linha', 0),
                coluna=pos_data.get('coluna', 0),
                numero_grupo=numero_grupo,
                posicao_no_grupo=pos_data.get('posicao_no_grupo', 0)
            )
            posicoes_criadas.append(posicao)
        
        return Response({
            "message": "Posições atualizadas com sucesso",
            "total": len(posicoes_criadas),
            "posicoes": PosicaoAlunoSerializer(posicoes_criadas, many=True).data
        })

class ProfessorObjetosSalaView(APIView):
    permission_classes = [IsAuthenticated, IsProfessor]
    
    def put(self, request, uuid):
        """Atualiza objetos da sala"""
        mapeamento = get_object_or_404(MapeamentoSala, uuid=uuid)
        
        serializer = AtualizarObjetosSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        objetos = serializer.validated_data['objetos']
        mapeamento.objetos_sala = objetos
        mapeamento.save()
        
        return Response({
            "message": "Objetos atualizados com sucesso",
            "objetos": objetos
        })

class ProfessorOrganizarAutomaticoView(APIView):
    permission_classes = [IsAuthenticated, IsProfessor]
    
    def post(self, request, uuid):
        """Organiza alunos automaticamente usando IA"""
        mapeamento = get_object_or_404(MapeamentoSala, uuid=uuid)
        
        # Busca todos estudantes da turma
        estudantes = list(Estudante.objects.filter(turma=mapeamento.turma))
        
        if not estudantes:
            return Response(
                {"error": "Turma não possui estudantes"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Usa serviço de IA
        ia_service = IAMapeamentoSala(mapeamento)
        posicoes_sugeridas = ia_service.organizar_automaticamente()
        
        # Remove posições antigas
        PosicaoAluno.objects.filter(mapeamento=mapeamento).delete()
        
        # Cria novas posições
        posicoes_criadas = []
        for pos_data in posicoes_sugeridas:
            estudante = pos_data['estudante']
            linha = pos_data['linha']
            coluna = pos_data['coluna']
            grupo = pos_data.get('grupo', 0)
            
            # Calcula número do grupo e posição no grupo
            alunos_por_grupo = mapeamento.alunos_por_grupo or 1
            if alunos_por_grupo > 1:
                numero_grupo = grupo
                posicao_no_grupo = grupo % alunos_por_grupo
            else:
                numero_grupo = None
                posicao_no_grupo = 0
            
            posicao = PosicaoAluno.objects.create(
                mapeamento=mapeamento,
                estudante=estudante,
                linha=linha,
                coluna=coluna,
                numero_grupo=numero_grupo,
                posicao_no_grupo=posicao_no_grupo,
                eh_lider=pos_data.get('eh_lider', False)
            )
            posicoes_criadas.append(posicao)
        
        return Response({
            "message": "Organização automática concluída",
            "posicoes": PosicaoAlunoSerializer(posicoes_criadas, many=True).data,
            "total": len(posicoes_criadas)
        })

class TemplatesSalaView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Lista templates disponíveis"""
        templates = TemplatesSala.objects.filter(publico=True).order_by('tipo_sala', 'nome')
        serializer = TemplatesSalaSerializer(templates, many=True)
        return Response(serializer.data)

# ==================== VIEWS LEGADAS (COMPATIBILIDADE) ====================

class GerarMapeamentoView(APIView):
    permission_classes = [IsProfessorOrPDTOrAdmin]

    def post(self, request):
        try:
            turma_id = request.data.get("turma_id")
            nome = request.data.get("nome", "Mapeamento Automático")
            linhas = int(request.data.get("linhas", 4))
            colunas = int(request.data.get("colunas", 5))
            turma = get_object_or_404(Turma, id=turma_id)
            mapeamento = gerar_novo_mapeamento(turma, turma.escola, nome, linhas, colunas)
            return Response(MapeamentoSerializer(mapeamento).data)
        except Exception as e:
            return Response({"erro": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class MapeamentoAtualView(APIView):
    permission_classes = [IsProfessorOrPDTOrAdmin]

    def get(self, request, uuid):
        mapeamento = get_object_or_404(MapeamentoSala, uuid=uuid)
        return Response(MapeamentoSerializer(mapeamento).data)

class MoverAlunoView(APIView):
    permission_classes = [IsProfessorOrPDTOrAdmin]

    def patch(self, request):
        serializer = MoverAlunoSerializer(data=request.data)
        if serializer.is_valid():
            estudante_id = serializer.validated_data["estudante_id"]
            nova_linha = serializer.validated_data["nova_linha"]
            nova_coluna = serializer.validated_data["nova_coluna"]
            posicao = get_object_or_404(PosicaoAluno, estudante_id=estudante_id)
            posicao.linha = nova_linha
            posicao.coluna = nova_coluna
            if 'novo_grupo' in serializer.validated_data:
                posicao.numero_grupo = serializer.validated_data["novo_grupo"]
                posicao.grupo = posicao.numero_grupo
            posicao.save()
            return Response({"mensagem": "Posição atualizada com sucesso"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class HistoricoMapeamentosView(APIView):
    permission_classes = [IsProfessorOrPDTOrAdmin]

    def get(self, request, turma_id):
        historico = MapeamentoSala.objects.filter(turma_id=turma_id).order_by("-criado_em")
        return Response(MapeamentoSerializer(historico, many=True).data)

class AlterarGrupoView(APIView):
    permission_classes = [IsProfessorOrPDTOrAdmin]

    def patch(self, request):
        estudante_id = request.data.get('estudante_id')
        novo_grupo = request.data.get('novo_grupo')
        posicao = get_object_or_404(PosicaoAluno, estudante_id=estudante_id)
        posicao.numero_grupo = novo_grupo
        posicao.grupo = novo_grupo
        posicao.save()
        return Response({"mensagem": "Grupo atualizado com sucesso"})
