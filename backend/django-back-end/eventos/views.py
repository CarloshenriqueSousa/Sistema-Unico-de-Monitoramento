# eventos/views.py
from rest_framework import viewsets, filters, permissions, status
from rest_framework.response import Response
from .models import Evento, InscricaoEvento
from .serializers import EventoSerializer, InscricaoEventoSerializer
from core.permissions import IsEscola, IsAluno, IsProfessor, IsPDT
from estudantes.models import Estudante

class EventoViewSet(viewsets.ModelViewSet):
    serializer_class = EventoSerializer
    permission_classes = [permissions.IsAuthenticated, IsEscola | IsAluno | IsProfessor | IsPDT]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['titulo', 'descricao', 'escola__nome']
    ordering_fields = ['data_inicio', 'data_fim']

    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'escola':
            # Escolas veem seus próprios eventos
            from escola.models import Escola
            try:
                escola = Escola.objects.get(usuario=user)
                return Evento.objects.filter(escola=escola)
            except Escola.DoesNotExist:
                return Evento.objects.none()
        elif user.user_type == 'aluno':
            try:
                estudante = Estudante.objects.get(usuario=user)
                return Evento.objects.filter(inscricoes__estudante=estudante)
            except Estudante.DoesNotExist:
                return Evento.objects.none()
        elif user.user_type in ('professor', 'pdt'):  # PDT é um tipo de professor
            return Evento.objects.all()
        return Evento.objects.none()

    def perform_create(self, serializer):
        user = self.request.user
        if user.user_type != 'escola':
            raise permissions.PermissionDenied("Apenas escolas podem criar eventos.")
        from escola.models import Escola
        try:
            escola = Escola.objects.get(usuario=user)
            serializer.save(escola=escola)
        except Escola.DoesNotExist:
            raise permissions.PermissionDenied("Usuário não é uma escola.")

class InscricaoEventoViewSet(viewsets.ModelViewSet):
    serializer_class = InscricaoEventoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'aluno':
            try:
                estudante = Estudante.objects.get(usuario=user)
                return InscricaoEvento.objects.filter(estudante=estudante)
            except Estudante.DoesNotExist:
                return InscricaoEvento.objects.none()
        elif user.user_type == 'escola':
            from escola.models import Escola
            try:
                escola = Escola.objects.get(usuario=user)
                return InscricaoEvento.objects.filter(evento__escola=escola)
            except Escola.DoesNotExist:
                return InscricaoEvento.objects.none()
        return InscricaoEvento.objects.none()

    def perform_create(self, serializer):
        user = self.request.user
        if user.user_type != 'aluno':
            raise permissions.PermissionDenied("Apenas estudantes podem se inscrever em eventos.")
        try:
            estudante = Estudante.objects.get(usuario=user)
            serializer.save(estudante=estudante)
        except Estudante.DoesNotExist:
            raise permissions.PermissionDenied("Usuário não é um estudante.")

    def perform_update(self, serializer):
        instance = serializer.instance
        if self.request.user.user_type == 'escola':
            from escola.models import Escola
            try:
                escola = Escola.objects.get(usuario=self.request.user)
                if instance.evento.escola == escola:
                    serializer.save()
                else:
                    raise permissions.PermissionDenied("Apenas a escola criadora pode atualizar inscrições.")
            except Escola.DoesNotExist:
                raise permissions.PermissionDenied("Usuário não é uma escola.")
        else:
            raise permissions.PermissionDenied("Apenas a escola criadora pode atualizar inscrições.")