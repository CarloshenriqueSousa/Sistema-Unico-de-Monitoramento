# placement/urls.py
from django.urls import path
from .views import (
    # Demonstração
    DemoTemplatesView,
    DemoTemplateDetailView,
    # Aluno
    AlunoMapeamentoView,
    # Professor
    ProfessorMapeamentosListView,
    ProfessorMapeamentoCreateView,
    ProfessorMapeamentoDetailView,
    ProfessorPosicionarAlunosView,
    ProfessorObjetosSalaView,
    ProfessorOrganizarAutomaticoView,
    TemplatesSalaView,
    # Legadas (compatibilidade)
    GerarMapeamentoView,
    MapeamentoAtualView,
    MoverAlunoView,
    HistoricoMapeamentosView,
    AlterarGrupoView
)

app_name = 'placement'

urlpatterns = [
    # === DEMONSTRAÇÃO (Público) ===
    path("demo/templates/", DemoTemplatesView.as_view(), name="demo-templates"),
    path("demo/template/<int:pk>/", DemoTemplateDetailView.as_view(), name="demo-template-detail"),
    
    # === ALUNO ===
    path("aluno/mapeamento-atual/", AlunoMapeamentoView.as_view(), name="aluno-mapeamento"),
    
    # === PROFESSOR ===
    path("professor/mapeamentos/", ProfessorMapeamentosListView.as_view(), name="professor-mapeamentos"),
    path("professor/mapeamento/criar/", ProfessorMapeamentoCreateView.as_view(), name="professor-mapeamento-criar"),
    path("professor/mapeamento/<uuid:uuid>/", ProfessorMapeamentoDetailView.as_view(), name="professor-mapeamento-detail"),
    path("professor/mapeamento/<uuid:uuid>/posicoes/", ProfessorPosicionarAlunosView.as_view(), name="professor-posicionar"),
    path("professor/mapeamento/<uuid:uuid>/objetos/", ProfessorObjetosSalaView.as_view(), name="professor-objetos"),
    path("professor/mapeamento/<uuid:uuid>/organizar-automatico/", ProfessorOrganizarAutomaticoView.as_view(), name="professor-organizar-auto"),
    path("professor/templates-sala/", TemplatesSalaView.as_view(), name="templates-sala"),
    
    # === LEGADAS (Compatibilidade) ===
    path("gerar/", GerarMapeamentoView.as_view(), name="gerar"),
    path("atual/<uuid:uuid>/", MapeamentoAtualView.as_view(), name="atual"),
    path("mover/", MoverAlunoView.as_view(), name="mover"),
    path("historico/<int:turma_id>/", HistoricoMapeamentosView.as_view(), name="historico"),
    path("grupo/alterar/", AlterarGrupoView.as_view(), name="alterar_grupo"),
]