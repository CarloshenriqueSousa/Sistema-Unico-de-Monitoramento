# estudantes/serializers.py
from rest_framework import serializers
from .models import Estudante, Nota, Falta
from core.serializers import UserSerializer
from escola.serializers import TurmaSerializer

class EstudanteSerializer(serializers.ModelSerializer):
    usuario = UserSerializer(read_only=True)
    turma = TurmaSerializer(read_only=True)

    class Meta:
        model = Estudante
        fields = ['id', 'usuario', 'turma', 'dificuldade_visao', 'dificuldade_aprendizado', 'media_humanas', 'media_linguagens', 'media_exatas', 'dots_pontos', 'dots_detalhes']
        read_only_fields = ['id', 'media_humanas', 'media_linguagens', 'media_exatas', 'dots_pontos', 'dots_detalhes']

class NotaSerializer(serializers.ModelSerializer):
    estudante = EstudanteSerializer(read_only=True)

    class Meta:
        model = Nota
        fields = '__all__'

class FaltaSerializer(serializers.ModelSerializer):
    estudante = EstudanteSerializer(read_only=True)

    class Meta:
        model = Falta
        fields = '__all__'