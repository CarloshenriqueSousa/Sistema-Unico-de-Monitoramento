# eventos/models.py
from django.db import models
from core.models import User
from simple_history.models import HistoricalRecords

class Evento(models.Model):
    escola = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'user_type': 'escola'},
        related_name='eventos'
    )
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    data_inicio = models.DateTimeField()
    data_fim = models.DateTimeField()
    criado_em = models.DateTimeField(auto_now_add=True)
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.titulo} ({self.escola.nome})"

class InscricaoEvento(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('confirmada', 'Confirmada'),
        ('cancelada', 'Cancelada'),
    ]

    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name='inscricoes')
    estudante = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'tipo': 'aluno'},
        related_name='inscricoes_eventos'
    )
    data_inscricao = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
    history = HistoricalRecords()

    class Meta:
        unique_together = ('evento', 'estudante')

    def __str__(self):
        return f"{self.estudante.nome} em {self.evento.titulo} ({self.status})"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.status == 'confirmada':
            from estudantes.models import Estudante
            estudante = Estudante.objects.get(usuario=self.estudante)
            estudante.atualizar_dots('eventos_participados', 10)