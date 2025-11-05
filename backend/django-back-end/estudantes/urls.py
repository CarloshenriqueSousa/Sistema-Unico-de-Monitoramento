# estudantes/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EstudanteViewSet, NotaViewSet, FaltaViewSet, DashboardAlunoAPIView, LeaderboardAPIView

router = DefaultRouter()
router.register(r'estudantes', EstudanteViewSet)
router.register(r'notas', NotaViewSet)
router.register(r'faltas', FaltaViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('dashboard/', DashboardAlunoAPIView.as_view(), name='dashboard'),
    path('leaderboard/', LeaderboardAPIView.as_view(), name='leaderboard'),
]