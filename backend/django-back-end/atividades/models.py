# atividades/models.py
from django.db import models
from django.utils import timezone
from estudantes.models import Estudante
from professores.models import Professor
from escola.models import Turma
from simple_history.models import HistoricalRecords

class QuestaoBanco(models.Model):
    AREA_CHOICES = [
        ('MATEMATICA', 'Matemática'),
        ('PORTUGUES', 'Português'),
        ('HISTORIA', 'História'),
        ('GEOGRAFIA', 'Geografia'),
        ('CIENCIAS', 'Ciências'),
        ('FISICA', 'Física'),
        ('QUIMICA', 'Química'),
        ('BIOLOGIA', 'Biologia'),
        ('INGLES', 'Inglês'),
        ('EDUCACAO_FISICA', 'Educação Física'),
        ('ARTES', 'Artes'),
        ('FILOSOFIA', 'Filosofia'),
        ('SOCIOLOGIA', 'Sociologia'),
        ('LITERATURA', 'Literatura'),
        ('GENERAL', 'Geral')
    ]
    
    DIFICULDADE_CHOICES = [
        ('FACIL', 'Fácil'),
        ('MEDIO', 'Médio'),
        ('DIFICIL', 'Difícil'),
        ('MUITO_DIFICIL', 'Muito Difícil')
    ]
    
    TIPO_CHOICES = [
        ('MULTIPLA_ESCOLHA', 'Múltipla Escolha'),
        ('VERDADEIRO_FALSO', 'Verdadeiro/Falso'),
        ('DISSERTATIVA', 'Dissertativa'),
        ('COMPLETAR', 'Completar'),
        ('ASSOCIACAO', 'Associação'),
        ('ORDENACAO', 'Ordenação')
    ]
    
    conteudo = models.TextField()
    area = models.CharField(max_length=50, choices=AREA_CHOICES)
    dificuldade = models.CharField(max_length=20, choices=DIFICULDADE_CHOICES)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='MULTIPLA_ESCOLHA')
    resposta_correta = models.TextField()
    opcoes = models.JSONField(default=list)
    
    # Metadados
    escola = models.ForeignKey('escola.Escola', on_delete=models.CASCADE, related_name='questoes', null=True, blank=True)
    criado_por = models.ForeignKey('professores.Professor', on_delete=models.CASCADE, related_name='questoes_criadas', null=True, blank=True)
    padrao_sistema = models.BooleanField(default=False, help_text="Questão padrão do sistema")
    
    # Estatísticas
    vezes_utilizada = models.PositiveIntegerField(default=0)
    taxa_acerto = models.FloatField(default=0.0)
    
    # Tags para organização
    tags = models.JSONField(default=list, blank=True)
    
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    class Meta:
        ordering = ['-criado_em']
        indexes = [
            models.Index(fields=['area']),
            models.Index(fields=['dificuldade']),
            models.Index(fields=['tipo']),
            models.Index(fields=['padrao_sistema']),
        ]

    def __str__(self):
        return f"{self.area} - {self.dificuldade} - {self.conteudo[:50]}..."

    def marcar_utilizada(self, acertou=False):
        """Marca a questão como utilizada e atualiza estatísticas"""
        self.vezes_utilizada += 1
        if acertou:
            # Atualizar taxa de acerto
            total_respostas = self.vezes_utilizada
            acertos_anteriores = self.taxa_acerto * (total_respostas - 1)
            self.taxa_acerto = (acertos_anteriores + 1) / total_respostas
        else:
            # Atualizar taxa de acerto
            total_respostas = self.vezes_utilizada
            acertos_anteriores = self.taxa_acerto * (total_respostas - 1)
            self.taxa_acerto = acertos_anteriores / total_respostas
        self.save(update_fields=['vezes_utilizada', 'taxa_acerto'])

class Atividade(models.Model):
    QUIZ = 'quiz'
    UPLOAD = 'upload'
    FORUM = 'forum'
    VIDEO = 'video'
    ANOTACAO = 'anotacao'
    PROVA = 'prova'

    TIPOS = [
        (QUIZ, 'Quiz'),
        (UPLOAD, 'Upload de Arquivo'),
        (FORUM, 'Fórum de Discussão'),
        (VIDEO, 'Vídeo Interativo'),
        (ANOTACAO, 'Anotação'),
        (PROVA, 'Prova Opcional'),
    ]

    ATIVA = 'ativa'
    INATIVA = 'inativa'
    FINALIZADA = 'finalizada'

    STATUS = [
        (ATIVA, 'Ativa'),
        (INATIVA, 'Inativa'),
        (FINALIZADA, 'Finalizada'),
    ]

    titulo = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    data_inicio = models.DateTimeField()
    data_fim = models.DateTimeField()
    tipo = models.CharField(max_length=20, choices=TIPOS)
    status = models.CharField(max_length=20, choices=STATUS, default=ATIVA)
    criado_em = models.DateTimeField(auto_now_add=True)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE, related_name='atividades')
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, related_name='atividades')
    gerada_por_ia = models.BooleanField(default=False)
    questoes = models.ManyToManyField(QuestaoBanco, blank=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.titulo

    def is_aberto(self):
        agora = timezone.now()
        return self.data_inicio <= agora <= self.data_fim

class RespostaAtividade(models.Model):
    atividade = models.ForeignKey(Atividade, on_delete=models.CASCADE, related_name='respostas')
    estudante = models.ForeignKey(Estudante, on_delete=models.CASCADE, related_name='respostas_atividades')
    resposta = models.TextField()
    nota = models.FloatField(null=True, blank=True)
    data_envio = models.DateTimeField(auto_now_add=True)
    history = HistoricalRecords()

    class Meta:
        unique_together = ('atividade', 'estudante')

    def __str__(self):
        return f"{self.estudante.usuario.nome} → {self.atividade.titulo}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.nota is not None:
            self.estudante.atualizar_dots('atividades_concluidas', int(self.nota))