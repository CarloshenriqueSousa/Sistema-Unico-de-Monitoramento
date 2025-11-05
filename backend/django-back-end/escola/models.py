from django.db import models
from core.models import User
from simple_history.models import HistoricalRecords

class Escola(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'user_type': 'escola'})
    cnpj = models.CharField(max_length=18, unique=True)
    nome = models.CharField(max_length=200, blank=True)
    endereco = models.TextField(blank=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.usuario.nome or f"Escola {self.cnpj}"

    def save(self, *args, **kwargs):
        if self.usuario and not self.nome:
            self.nome = self.usuario.nome
        super().save(*args, **kwargs)

class Turma(models.Model):
    escola = models.ForeignKey(Escola, on_delete=models.CASCADE, related_name='turmas')
    nome = models.CharField(max_length=50)
    ano = models.PositiveIntegerField()
    capacidade = models.PositiveIntegerField(default=30)
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.nome} - {self.ano}º ano"

class Liberacao(models.Model):
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, related_name='liberacoes')
    tipo = models.CharField(max_length=50, choices=[('ALMOCO', 'Almoço'), ('RECREIO', 'Recreio'), ('SAIDA', 'Saída')])
    data_hora = models.DateTimeField()
    liberado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.tipo} para {self.turma} em {self.data_hora}"

class Jogo(models.Model):
    escola = models.ForeignKey(Escola, on_delete=models.CASCADE, related_name='jogos')
    nome = models.CharField(max_length=100)
    data = models.DateField()
    participantes = models.ManyToManyField('estudantes.Estudante', through='TimeJogo', blank=True)
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.nome} em {self.data}"

class TimeJogo(models.Model):
    jogo = models.ForeignKey(Jogo, on_delete=models.CASCADE)
    estudante = models.ForeignKey('estudantes.Estudante', on_delete=models.CASCADE)
    time_nome = models.CharField(max_length=50)
    pontos = models.IntegerField(default=0)