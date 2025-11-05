from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from estudantes.models import Estudante
from professores.models import Professor
from escola.models import Turma, Escola
from simple_history.models import HistoricalRecords
import uuid

class Agenda(models.Model):
    GRAU_IMPORTANCIA_CHOICES = [
        ('BAIXA', 'Baixa'),
        ('MEDIA', 'Média'),
        ('ALTA', 'Alta'),
        ('CRITICA', 'Crítica')
    ]
    
    TIPO_EVENTO_CHOICES = [
        ('ATIVIDADE', 'Atividade'),
        ('PROVA', 'Prova'),
        ('PARCIAL', 'Parcial'),
        ('TRABALHO', 'Trabalho'),
        ('APRESENTACAO', 'Apresentação'),
        ('REUNIAO', 'Reunião'),
        ('EVENTO_ESCOLA', 'Evento da Escola'),
        ('FERIADO', 'Feriado'),
        ('CUSTOMIZADO', 'Customizado')
    ]
    
    uuid = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    titulo = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    data_inicio = models.DateTimeField()
    data_fim = models.DateTimeField()
    tipo_evento = models.CharField(max_length=20, choices=TIPO_EVENTO_CHOICES)
    grau_importancia = models.CharField(max_length=10, choices=GRAU_IMPORTANCIA_CHOICES, default='MEDIA')
    
    # Relacionamentos
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, related_name='eventos_agenda', null=True, blank=True)
    escola = models.ForeignKey(Escola, on_delete=models.CASCADE, related_name='eventos_agenda')
    criado_por = models.ForeignKey(Professor, on_delete=models.CASCADE, related_name='eventos_criados')
    
    # Configurações de notificação
    notificar_antes = models.PositiveIntegerField(default=24, help_text="Horas antes do evento para notificar")
    notificacao_enviada = models.BooleanField(default=False)
    
    # Configurações de conflito
    permite_conflito = models.BooleanField(default=False)
    eventos_conflitantes = models.ManyToManyField('self', blank=True, symmetrical=True)
    
    # Campos customizados
    campos_customizados = models.JSONField(default=dict, blank=True)
    
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    class Meta:
        ordering = ['data_inicio']
        indexes = [
            models.Index(fields=['data_inicio']),
            models.Index(fields=['grau_importancia']),
            models.Index(fields=['tipo_evento']),
        ]

    def __str__(self):
        return f"{self.titulo} - {self.data_inicio.strftime('%d/%m/%Y')}"

    def clean(self):
        if self.data_fim <= self.data_inicio:
            raise ValidationError("A data de fim deve ser posterior à data de início.")
        
        # Verificar conflitos se não permitir
        if not self.permite_conflito and self.grau_importancia in ['ALTA', 'CRITICA']:
            conflitos = self.verificar_conflitos()
            if conflitos:
                raise ValidationError(f"Existem conflitos com eventos: {', '.join([str(c) for c in conflitos])}")

    def verificar_conflitos(self):
        """Verifica se há conflitos com outros eventos"""
        if not self.pk:  # Novo evento
            eventos_conflitantes = Agenda.objects.filter(
                escola=self.escola,
                data_inicio__lt=self.data_fim,
                data_fim__gt=self.data_inicio,
                permite_conflito=False
            ).exclude(grau_importancia='BAIXA')
        else:  # Evento existente
            eventos_conflitantes = Agenda.objects.filter(
                escola=self.escola,
                data_inicio__lt=self.data_fim,
                data_fim__gt=self.data_inicio,
                permite_conflito=False
            ).exclude(pk=self.pk).exclude(grau_importancia='BAIXA')
        
        return list(eventos_conflitantes)

    def marcar_notificacao_enviada(self):
        self.notificacao_enviada = True
        self.save(update_fields=['notificacao_enviada'])
    
    def deve_notificar(self):
        """Retorna True se o evento deve ser notificado baseado em sua importância"""
        agora = timezone.now()
        tempo_restante = (self.data_inicio - agora).total_seconds() / 3600  # horas
        
        # Definir horários padrão baseado na importância
        if self.grau_importancia == 'CRITICA':
            return tempo_restante <= 72 and not self.notificacao_enviada
        elif self.grau_importancia == 'ALTA':
            return tempo_restante <= 48 and not self.notificacao_enviada
        elif self.grau_importancia == 'MEDIA':
            return tempo_restante <= 24 and not self.notificacao_enviada
        else:  # BAIXA
            return tempo_restante <= 2 and not self.notificacao_enviada
    
    def obter_mensagem_notificacao(self):
        """Gera mensagem de notificação baseada no tipo e importância"""
        emojis = {
            'PROVA': '📝',
            'PARCIAL': '📊',
            'ATIVIDADE': '📚',
            'TRABALHO': '📋',
            'APRESENTACAO': '🎤',
            'REUNIAO': '👥',
            'EVENTO_ESCOLA': '🎉',
            'FERIADO': '🎊'
        }
        
        emoji = emojis.get(self.tipo_evento, '📅')
        importancia_emoji = {
            'CRITICA': '🔥',
            'ALTA': '⚠️',
            'MEDIA': '📌',
            'BAIXA': 'ℹ️'
        }
        
        importancia = importancia_emoji.get(self.grau_importancia, '')
        
        mensagem = f"{emoji} {importancia} {self.titulo}\n"
        mensagem += f"📅 Data: {self.data_inicio.strftime('%d/%m/%Y às %H:%M')}\n"
        
        if self.descricao:
            mensagem += f"📝 {self.descricao[:100]}...\n"
        
        if self.grau_importancia in ['CRITICA', 'ALTA']:
            mensagem += f"\n⚠️ Evento de {self.get_grau_importancia_display().lower()}!"
        
        return mensagem
    
    def tem_conflitos_criticos(self):
        """Verifica se há conflitos críticos com outros eventos"""
        conflitos = self.verificar_conflitos()
        return any(e.grau_importancia in ['CRITICA', 'ALTA'] for e in conflitos)
    
    def pode_ser_remarcado(self):
        """Verifica se o evento pode ser remarcado"""
        agora = timezone.now()
        return self.data_inicio > agora and self.grau_importancia != 'CRITICA'

class NotificacaoAgenda(models.Model):
    TIPO_NOTIFICACAO_CHOICES = [
        ('EMAIL', 'E-mail'),
        ('SMS', 'SMS'),
        ('PUSH', 'Push Notification'),
        ('SISTEMA', 'Notificação do Sistema')
    ]
    
    evento = models.ForeignKey(Agenda, on_delete=models.CASCADE, related_name='notificacoes')
    destinatario = models.ForeignKey('core.User', on_delete=models.CASCADE, related_name='notificacoes_agenda')
    tipo_notificacao = models.CharField(max_length=20, choices=TIPO_NOTIFICACAO_CHOICES)
    mensagem = models.TextField()
    enviada = models.BooleanField(default=False)
    data_envio = models.DateTimeField(null=True, blank=True)
    data_agendada = models.DateTimeField()
    history = HistoricalRecords()

    class Meta:
        ordering = ['-data_agendada']
        unique_together = ('evento', 'destinatario', 'data_agendada')

    def __str__(self):
        return f"{self.evento.titulo} → {self.destinatario.nome}"

class ConfiguracaoAgenda(models.Model):
    escola = models.OneToOneField(Escola, on_delete=models.CASCADE, related_name='config_agenda')
    
    # Configurações de notificação
    notificar_professores = models.BooleanField(default=True)
    notificar_alunos = models.BooleanField(default=True)
    notificar_pais = models.BooleanField(default=False)
    
    # Horários de notificação padrão
    notificacao_alta_importancia = models.PositiveIntegerField(default=48, help_text="Horas antes para eventos de alta importância")
    notificacao_media_importancia = models.PositiveIntegerField(default=24, help_text="Horas antes para eventos de média importância")
    notificacao_baixa_importancia = models.PositiveIntegerField(default=2, help_text="Horas antes para eventos de baixa importância")
    
    # Configurações de conflito
    verificar_conflitos_automaticamente = models.BooleanField(default=True)
    bloquear_conflitos_criticos = models.BooleanField(default=True)
    
    # Campos customizados para eventos
    campos_personalizados = models.JSONField(default=dict, blank=True)
    
    history = HistoricalRecords()

    def __str__(self):
        return f"Configuração Agenda - {self.escola.nome}"
