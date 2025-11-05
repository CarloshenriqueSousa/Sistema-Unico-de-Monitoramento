# professores/models.py
from django.db import models
from core.models import User
from simple_history.models import HistoricalRecords
from escola.models import Turma, Escola

class Professor(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'user_type': 'professor'})
    escola = models.ForeignKey(Escola, on_delete=models.CASCADE, related_name='professores')
    turmas = models.ManyToManyField(Turma, related_name='professores')
    history = HistoricalRecords()

    def __str__(self):
        return f"Professor {self.usuario.nome}"

class PDT(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'user_type': 'professor'})  # PDT é um tipo de professor
    escola = models.ForeignKey(Escola, on_delete=models.CASCADE, related_name='pdts')
    turma = models.OneToOneField(Turma, on_delete=models.CASCADE, related_name='pdt')
    history = HistoricalRecords()

    def __str__(self):
        return f"PDT {self.usuario.nome} - {self.turma.nome}"