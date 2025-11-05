# eventos/admin.py
from django.contrib import admin
from .models import Evento, InscricaoEvento
from simple_history.admin import SimpleHistoryAdmin

@admin.register(Evento)
class EventoAdmin(SimpleHistoryAdmin):
    list_display = ('titulo', 'escola', 'data_inicio', 'data_fim')
    search_fields = ('titulo', 'descricao')
    list_filter = ('escola', 'data_inicio')

@admin.register(InscricaoEvento)
class InscricaoEventoAdmin(SimpleHistoryAdmin):
    list_display = ('estudante', 'evento', 'status', 'data_inscricao')
    list_filter = ('status', 'evento')
    search_fields = ('estudante__nome', 'evento__titulo')