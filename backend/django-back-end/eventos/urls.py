# eventos/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EventoViewSet, InscricaoEventoViewSet

router = DefaultRouter()
router.register(r'eventos', EventoViewSet, basename='evento')
router.register(r'inscricoes', InscricaoEventoViewSet, basename='inscricao')

urlpatterns = [
    path('', include(router.urls)),
]