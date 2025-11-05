# escola/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    EscolaViewSet, TurmaViewSet, LiberacaoViewSet, JogoViewSet, TimeJogoViewSet,
    PreCadastroAlunoAPIView, PreCadastroProfessorAPIView, DashboardEscolaAPIView
)

router = DefaultRouter()
router.register(r'escolas', EscolaViewSet)
router.register(r'turmas', TurmaViewSet)
router.register(r'liberacoes', LiberacaoViewSet)
router.register(r'jogos', JogoViewSet)
router.register(r'times-jogo', TimeJogoViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('precadastro-aluno/', PreCadastroAlunoAPIView.as_view(), name='precadastro_aluno'),
    path('precadastro-professor/', PreCadastroProfessorAPIView.as_view(), name='precadastro_professor'),
    path('dashboard/', DashboardEscolaAPIView.as_view(), name='dashboard_escola'),
]