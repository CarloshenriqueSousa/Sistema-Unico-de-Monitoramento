# agenda/admin.py
from django.contrib import admin
from .models import Agenda, NotificacaoAgenda, ConfiguracaoAgenda
from simple_history.admin import SimpleHistoryAdmin


@admin.register(Agenda)
class AgendaAdmin(SimpleHistoryAdmin):
    list_display = ('titulo', 'tipo_evento', 'grau_importancia', 'data_inicio', 'turma', 'criado_por')
    list_filter = ('tipo_evento', 'grau_importancia', 'data_inicio', 'permite_conflito')
    search_fields = ('titulo', 'descricao')
    date_hierarchy = 'data_inicio'
    readonly_fields = ('criado_em', 'atualizado_em')
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('titulo', 'descricao', 'tipo_evento', 'grau_importancia')
        }),
        ('Datas', {
            'fields': ('data_inicio', 'data_fim')
        }),
        ('Relacionamentos', {
            'fields': ('turma', 'escola', 'criado_por')
        }),
        ('Configurações de Notificação', {
            'fields': ('notificar_antes', 'notificacao_enviada')
        }),
        ('Configurações de Conflito', {
            'fields': ('permite_conflito', 'eventos_conflitantes')
        }),
        ('Campos Customizados', {
            'fields': ('campos_customizados',)
        }),
        ('Metadados', {
            'fields': ('criado_em', 'atualizado_em'),
            'classes': ('collapse',)
        })
    )


@admin.register(NotificacaoAgenda)
class NotificacaoAgendaAdmin(SimpleHistoryAdmin):
    list_display = ('evento', 'destinatario', 'tipo_notificacao', 'enviada', 'data_agendada')
    list_filter = ('tipo_notificacao', 'enviada', 'data_agendada')
    search_fields = ('evento__titulo', 'destinatario__nome')
    date_hierarchy = 'data_agendada'
    readonly_fields = ('data_envio',)


@admin.register(ConfiguracaoAgenda)
class ConfiguracaoAgendaAdmin(SimpleHistoryAdmin):
    list_display = ('escola', 'verificar_conflitos_automaticamente', 'bloquear_conflitos_criticos')
    list_filter = ('verificar_conflitos_automaticamente', 'bloquear_conflitos_criticos')
    search_fields = ('escola__nome',)
