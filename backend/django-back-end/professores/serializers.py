# professores/serializers.py
from rest_framework import serializers
from .models import Professor, PDT
from core.serializers import UserSerializer
from escola.serializers import TurmaSerializer, EscolaSerializer

class ProfessorSerializer(serializers.ModelSerializer):
    usuario = UserSerializer(read_only=True)
    escola = EscolaSerializer(read_only=True)
    turmas = TurmaSerializer(many=True, read_only=True)

    class Meta:
        model = Professor
        fields = ['id', 'usuario', 'escola', 'turmas']
        read_only_fields = ['id']

class PDTSerializer(serializers.ModelSerializer):
    usuario = UserSerializer(read_only=True)
    escola = EscolaSerializer(read_only=True)
    turma = TurmaSerializer(read_only=True)

    class Meta:
        model = PDT
        fields = ['id', 'usuario', 'escola', 'turma']
        read_only_fields = ['id']