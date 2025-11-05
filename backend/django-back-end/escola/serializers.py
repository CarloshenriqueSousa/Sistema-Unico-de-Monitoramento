# escola/serializers.py
from rest_framework import serializers
from .models import Escola, Turma, Liberacao, Jogo, TimeJogo
from core.serializers import UserSerializer

class EscolaSerializer(serializers.ModelSerializer):
    usuario = UserSerializer(read_only=True)

    class Meta:
        model = Escola
        fields = ['id', 'usuario', 'cnpj', 'nome', 'endereco']
        read_only_fields = ['id']

class TurmaSerializer(serializers.ModelSerializer):
    escola = EscolaSerializer(read_only=True)

    class Meta:
        model = Turma
        fields = ['id', 'escola', 'nome', 'ano', 'capacidade']
        read_only_fields = ['id']

class LiberacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Liberacao
        fields = '__all__'

class JogoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jogo
        fields = '__all__'

class TimeJogoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeJogo
        fields = '__all__'