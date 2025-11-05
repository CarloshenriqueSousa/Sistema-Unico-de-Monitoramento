# atividades/admin.py
from django.contrib import admin
from .models import Atividade, RespostaAtividade, QuestaoBanco
from simple_history.admin import SimpleHistoryAdmin

@admin.register(Atividade)
class AtividadeAdmin(SimpleHistoryAdmin):
    list_display = ('titulo', 'tipo', 'status', 'professor', 'turma', 'gerada_por_ia')
    list_filter = ('tipo', 'status', 'gerada_por_ia')
    search_fields = ('titulo', 'descricao')

@admin.register(RespostaAtividade)
class RespostaAtividadeAdmin(SimpleHistoryAdmin):
    list_display = ('atividade', 'estudante', 'nota', 'data_envio')
    list_filter = ('atividade',)
    search_fields = ('estudante__usuario__nome',)

@admin.register(QuestaoBanco)
class QuestaoBancoAdmin(SimpleHistoryAdmin):
    list_display = ('conteudo', 'area', 'dificuldade')
    list_filter = ('area', 'dificuldade')
    search_fields = ('conteudo',)