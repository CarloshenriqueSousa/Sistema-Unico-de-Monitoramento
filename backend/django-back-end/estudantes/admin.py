# estudantes/admin.py
from django.contrib import admin
from .models import (
    Estudante, Nota, Falta, LiderSala, Frequencia, ConfiguracaoEscola,
    ConfiguracaoLiderancaTurma, ConfiguracaoDOT, TarefaDot, ObservacaoDot, RelatorioDot
)
from simple_history.admin import SimpleHistoryAdmin


@admin.register(Estudante)
class EstudanteAdmin(SimpleHistoryAdmin):
    list_display = ('usuario', 'turma', 'dificuldade_visao', 'dificuldade_aprendizado', 'eh_lider', 'dots_pontos')
    search_fields = ('usuario__nome',)
    list_filter = ('dificuldade_visao', 'dificuldade_aprendizado', 'eh_lider')


@admin.register(Nota)
class NotaAdmin(SimpleHistoryAdmin):
    list_display = ('estudante', 'materia', 'nota_global', 'area')
    list_filter = ('area',)


@admin.register(Falta)
class FaltaAdmin(SimpleHistoryAdmin):
    list_display = ('estudante', 'data', 'aula')
    list_filter = ('data',)


@admin.register(LiderSala)
class LiderSalaAdmin(SimpleHistoryAdmin):
    list_display = ('estudante', 'turma', 'cargo', 'ativo', 'pode_registrar_frequencia')
    list_filter = ('cargo', 'ativo', 'turma')
    search_fields = ('estudante__usuario__nome',)


@admin.register(Frequencia)
class FrequenciaAdmin(SimpleHistoryAdmin):
    list_display = ('turma', 'data', 'aula', 'registrado_por')
    list_filter = ('data', 'turma')
    date_hierarchy = 'data'


@admin.register(ConfiguracaoEscola)
class ConfiguracaoEscolaAdmin(SimpleHistoryAdmin):
    list_display = ('escola', 'campo_nome', 'campo_tipo', 'obrigatorio', 'ativo')
    list_filter = ('campo_tipo', 'obrigatorio', 'ativo')


@admin.register(ConfiguracaoLiderancaTurma)
class ConfiguracaoLiderancaTurmaAdmin(SimpleHistoryAdmin):
    list_display = ('turma', 'max_representantes', 'max_monitores', 'permitir_cargos_customizados')
    search_fields = ('turma__nome',)


@admin.register(ConfiguracaoDOT)
class ConfiguracaoDOTAdmin(SimpleHistoryAdmin):
    list_display = ('titulo', 'professor', 'tipo', 'ativo', 'calcular_pontos')
    list_filter = ('tipo', 'ativo', 'calcular_pontos')
    search_fields = ('titulo', 'descricao')


@admin.register(TarefaDot)
class TarefaDotAdmin(SimpleHistoryAdmin):
    list_display = ('titulo', 'estudante', 'configuracao', 'status', 'prioridade', 'data_vencimento')
    list_filter = ('status', 'prioridade', 'data_vencimento')
    search_fields = ('titulo', 'estudante__usuario__nome')
    date_hierarchy = 'data_criacao'


@admin.register(ObservacaoDot)
class ObservacaoDotAdmin(SimpleHistoryAdmin):
    list_display = ('titulo', 'estudante', 'professor', 'data_observacao', 'privada')
    list_filter = ('privada', 'data_observacao')
    search_fields = ('titulo', 'estudante__usuario__nome')
    date_hierarchy = 'data_observacao'


@admin.register(RelatorioDot)
class RelatorioDotAdmin(SimpleHistoryAdmin):
    list_display = ('titulo', 'tipo', 'professor', 'data_geracao')
    list_filter = ('tipo', 'data_geracao')
    search_fields = ('titulo',)
    date_hierarchy = 'data_geracao'