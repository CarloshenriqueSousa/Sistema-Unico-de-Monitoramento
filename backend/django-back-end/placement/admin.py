# placement/admin.py
from django.contrib import admin
from .models import MapeamentoSala, PosicaoAluno, TemplatesSala
from simple_history.admin import SimpleHistoryAdmin

@admin.register(MapeamentoSala)
class MapeamentoSalaAdmin(SimpleHistoryAdmin):
    list_display = ('nome', 'turma', 'fileiras_verticais', 'fileiras_horizontais', 'tipo_sala', 'ativo', 'criado_em')
    list_filter = ('turma', 'escola', 'tipo_sala', 'ativo')
    search_fields = ('nome', 'turma__nome')
    readonly_fields = ('uuid', 'criado_em', 'atualizado_em')

@admin.register(PosicaoAluno)
class PosicaoAlunoAdmin(admin.ModelAdmin):
    list_display = ('mapeamento', 'estudante', 'linha', 'coluna', 'numero_grupo', 'fixo')
    list_filter = ('mapeamento', 'fixo', 'eh_lider')

@admin.register(TemplatesSala)
class TemplatesSalaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo_sala', 'publico', 'criado_em')
    list_filter = ('tipo_sala', 'publico')
    search_fields = ('nome', 'descricao')