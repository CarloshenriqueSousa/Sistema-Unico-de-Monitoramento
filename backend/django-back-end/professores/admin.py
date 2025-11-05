# professores/admin.py
from django.contrib import admin
from .models import Professor, PDT
from simple_history.admin import SimpleHistoryAdmin

@admin.register(Professor)
class ProfessorAdmin(SimpleHistoryAdmin):
    list_display = ('usuario', 'escola')
    search_fields = ('usuario__nome',)

@admin.register(PDT)
class PDTAdmin(SimpleHistoryAdmin):
    list_display = ('usuario', 'escola', 'turma')
    search_fields = ('usuario__nome',)