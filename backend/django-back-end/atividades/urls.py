# atividades/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AtividadeViewSet, RespostaAtividadeViewSet, QuestaoBancoViewSet, GerarAtividadeIAView

router = DefaultRouter()
router.register(r'atividades', AtividadeViewSet)
router.register(r'respostas', RespostaAtividadeViewSet, basename='resposta-atividade')
router.register(r'questoes-banco', QuestaoBancoViewSet, basename='questao-banco')

urlpatterns = [
    path('', include(router.urls)),
    path('gerar-ia/', GerarAtividadeIAView.as_view(), name='gerar_atividade_ia'),
]
