# placement/serializers.py
from rest_framework import serializers
from .models import MapeamentoSala, PosicaoAluno, TemplatesSala
from estudantes.serializers import EstudanteSerializer
from escola.serializers import TurmaSerializer

class PosicaoAlunoSerializer(serializers.ModelSerializer):
    estudante = EstudanteSerializer(read_only=True)
    estudante_id = serializers.IntegerField(write_only=True, required=False)
    
    class Meta:
        model = PosicaoAluno
        fields = [
            'id', 
            'estudante', 
            'estudante_id',
            'linha', 
            'coluna', 
            'numero_grupo',
            'posicao_no_grupo',
            'grupo',  # Legado
            'fixo',
            'eh_lider',
            'observacoes',
            'posicionado_em',
            'atualizado_em'
        ]
        read_only_fields = ['id', 'posicionado_em', 'atualizado_em']

class MapeamentoSerializer(serializers.ModelSerializer):
    posicoes = PosicaoAlunoSerializer(many=True, read_only=True)
    turma_nome = serializers.CharField(source='turma.nome', read_only=True)
    escola_nome = serializers.CharField(source='escola.usuario.nome', read_only=True)
    
    class Meta:
        model = MapeamentoSala
        fields = [
            'uuid',
            'nome',
            'turma',
            'turma_nome',
            'escola',
            'escola_nome',
            'fileiras_verticais',
            'fileiras_horizontais',
            'alunos_por_grupo',
            'tipo_sala',
            'layout_config',
            'objetos_sala',
            'cor_fundo',
            'mostrar_grade',
            'mostrar_numeros',
            'ativo',
            'usar_sistema_lideres',
            'posicionamento_lideres',
            'usar_ia_automatica',
            'criterios_ia',
            'modo_edicao',
            'posicoes',
            'criado_em',
            'atualizado_em',
            # Legados (para compatibilidade)
            'linhas',
            'colunas',
            'tipo_agrupamento',
            'numero_pessoas_grupo'
        ]
        read_only_fields = ['uuid', 'criado_em', 'atualizado_em', 'escola']
    
    def validate(self, data):
        if self.instance:
            linhas = data.get('fileiras_verticais', self.instance.fileiras_verticais or self.instance.linhas)
            colunas = data.get('fileiras_horizontais', self.instance.fileiras_horizontais or self.instance.colunas)
            alunos_por_grupo = data.get('alunos_por_grupo', self.instance.alunos_por_grupo or 1)
            capacidade = linhas * colunas * alunos_por_grupo
            count = self.instance.posicoes.count()
            
            if count > capacidade:
                raise serializers.ValidationError(
                    f"Capacidade insuficiente: {capacidade} assentos para {count} alunos alocados."
                )
        return data

class MoverAlunoSerializer(serializers.Serializer):
    estudante_id = serializers.IntegerField()
    nova_linha = serializers.IntegerField(min_value=0)
    nova_coluna = serializers.IntegerField(min_value=0)
    novo_grupo = serializers.IntegerField(min_value=0, required=False, allow_null=True)
    posicao_no_grupo = serializers.IntegerField(min_value=0, required=False, default=0)

class AtualizarPosicoesSerializer(serializers.Serializer):
    posicoes = serializers.ListField(
        child=serializers.DictField(),
        required=True
    )

class AtualizarObjetosSerializer(serializers.Serializer):
    objetos = serializers.ListField(
        child=serializers.DictField(),
        required=True
    )

class TemplatesSalaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemplatesSala
        fields = [
            'id',
            'nome',
            'tipo_sala',
            'descricao',
            'config',
            'publico',
            'criado_em',
            'atualizado_em'
        ]
        read_only_fields = ['id', 'criado_em', 'atualizado_em']
