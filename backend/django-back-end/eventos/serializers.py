from rest_framework import serializers
from .models import Evento, InscricaoEvento
from core.models import User

class InscricaoEventoSerializer(serializers.ModelSerializer):
    estudante_nome = serializers.CharField(source='estudante.usuario.nome', read_only=True)
    
    class Meta:
        model = InscricaoEvento
        fields = ['id', 'estudante', 'estudante_nome', 'data_inscricao', 'presente']

class EventoSerializer(serializers.ModelSerializer):
    escola_nome = serializers.CharField(source='escola.usuario.nome', read_only=True)
    inscricoes = InscricaoEventoSerializer(many=True, read_only=True)
    
    class Meta:
        model = Evento
        fields = [
            'id', 'escola', 'escola_nome', 'titulo', 'descricao', 
            'data_inicio', 'data_fim', 'local', 'tipo', 
            'capacidade_maxima', 'inscricoes_abertas', 'inscricoes'
        ]

class InscricaoEventoCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = InscricaoEvento
        fields = ['id', 'estudante', 'evento', 'data_inscricao', 'presente']
        read_only_fields = ['data_inscricao']
