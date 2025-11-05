# escola/admin.py
from django.contrib import admin
from .models import Escola, Turma, Liberacao, Jogo, TimeJogo
from simple_history.admin import SimpleHistoryAdmin

@admin.register(Escola)
class EscolaAdmin(SimpleHistoryAdmin):
    list_display = ('nome', 'cnpj', 'usuario')
    search_fields = ('nome', 'cnpj')

@admin.register(Turma)
class TurmaAdmin(SimpleHistoryAdmin):
    list_display = ('nome', 'ano', 'escola')
    list_filter = ('escola',)

@admin.register(Liberacao)
class LiberacaoAdmin(SimpleHistoryAdmin):
    list_display = ('tipo', 'data_hora', 'turma')

@admin.register(Jogo)
class JogoAdmin(SimpleHistoryAdmin):
    list_display = ('nome', 'data', 'escola')

@admin.register(TimeJogo)
class TimeJogoAdmin(admin.ModelAdmin):
    list_display = ('jogo', 'estudante', 'time_nome', 'pontos')