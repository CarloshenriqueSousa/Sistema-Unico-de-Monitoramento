# atividades/serializers.py
from rest_framework import serializers
from .models import Atividade, RespostaAtividade, QuestaoBanco
from professores.serializers import ProfessorSerializer
from escola.serializers import TurmaSerializer
from estudantes.serializers import EstudanteSerializer

class QuestaoBancoSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestaoBanco
        fields = '__all__'

class AtividadeSerializer(serializers.ModelSerializer):
    professor = ProfessorSerializer(read_only=True)
    turma = TurmaSerializer(read_only=True)
    questoes = QuestaoBancoSerializer(many=True, read_only=True)

    class Meta:
        model = Atividade
        fields = ['id', 'titulo', 'descricao', 'data_inicio', 'data_fim', 'tipo', 'status', 'professor', 'turma', 'gerada_por_ia', 'questoes']

    def validate(self, attrs):
        if attrs['data_fim'] < attrs['data_inicio']:
            raise serializers.ValidationError("Data de término deve ser posterior à data de início.")
        return attrs

class RespostaAtividadeSerializer(serializers.ModelSerializer):
    estudante = EstudanteSerializer(read_only=True)
    atividade = AtividadeSerializer(read_only=True)

    class Meta:
        model = RespostaAtividade
        fields = ['id', 'atividade', 'estudante', 'resposta', 'nota', 'data_envio']

    def validate_nota(self, value):
        if value is not None and not (0 <= value <= 100):
            raise serializers.ValidationError("Nota deve estar entre 0 e 100.")
        return value