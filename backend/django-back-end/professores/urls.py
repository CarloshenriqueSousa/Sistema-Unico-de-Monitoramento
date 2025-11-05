# professores/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProfessorViewSet, PDTViewSet, DashboardProfessorAPIView, EditarMapeamentoAPIView, CriarAtividadeAPIView

router = DefaultRouter()
router.register(r'professores', ProfessorViewSet)
router.register(r'pdts', PDTViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('dashboard/', DashboardProfessorAPIView.as_view(), name='dashboard'),
    path('mapeamento/editar/<int:turma_id>/', EditarMapeamentoAPIView.as_view(), name='editar_mapeamento'),
    path('atividades/criar/', CriarAtividadeAPIView.as_view(), name='criar_atividade'),
]