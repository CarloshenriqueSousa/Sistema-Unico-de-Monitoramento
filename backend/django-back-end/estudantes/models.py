from django.db import models
from core.models import User
from escola.models import Turma
from simple_history.models import HistoricalRecords

class Estudante(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'user_type': 'aluno'})
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, related_name='estudantes')
    
    # Configurações iniciais obrigatórias
    dificuldade_aprendizado = models.CharField(
        max_length=50, 
        choices=[
            ('NENHUMA', 'Nenhuma'), 
            ('LEVE', 'Leve'), 
            ('MODERADA', 'Moderada'), 
            ('SEVERA', 'Severa')
        ], 
        default='NENHUMA'
    )
    dificuldade_visao = models.CharField(
        max_length=50, 
        choices=[
            ('NENHUMA', 'Nenhuma'), 
            ('BAIXA', 'Baixa'), 
            ('MEDIA', 'Média'), 
            ('ALTA', 'Alta')
        ], 
        default='NENHUMA'
    )
    altura = models.CharField(
        max_length=20,
        choices=[
            ('BAIXA', 'Baixa (até 1,50m)'),
            ('MEDIA', 'Média (1,51m - 1,70m)'),
            ('ALTA', 'Alta (acima de 1,70m)')
        ],
        default='MEDIA'
    )
    
    # Campos customizáveis pela escola
    configuracoes_customizadas = models.JSONField(default=dict, blank=True)
    
    # Campos acadêmicos
    media_humanas = models.FloatField(default=0.0)
    media_linguagens = models.FloatField(default=0.0)
    media_exatas = models.FloatField(default=0.0)
    dots_pontos = models.IntegerField(default=0)
    dots_detalhes = models.JSONField(default=dict)
    
    # Status de liderança
    eh_lider = models.BooleanField(default=False)
    cargo_lideranca = models.CharField(max_length=100, blank=True, null=True)
    data_nomeacao_lider = models.DateTimeField(blank=True, null=True)
    
    history = HistoricalRecords()

    def __str__(self):
        return self.usuario.nome

    def atualizar_dots(self, categoria, valor):
        self.dots_detalhes[categoria] = self.dots_detalhes.get(categoria, 0) + valor
        self.dots_pontos += valor
        self.save()

class Nota(models.Model):
    estudante = models.ForeignKey(Estudante, on_delete=models.CASCADE, related_name='notas')
    materia = models.CharField(max_length=100)
    area = models.CharField(max_length=50, choices=[('HUMANAS', 'Humanas'), ('LINGUAGENS', 'Linguagens'), ('EXATAS', 'Exatas')])
    nota_global = models.FloatField()
    nota_parcial1 = models.FloatField(null=True, blank=True)
    nota_parcial2 = models.FloatField(null=True, blank=True)
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.estudante} - {self.materia}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.estudante.atualizar_dots('notas', int(self.nota_global))
        self.atualizar_medias()

    def atualizar_medias(self):
        estudante = self.estudante
        if self.area == 'HUMANAS':
            notas_humanas = Nota.objects.filter(estudante=estudante, area='HUMANAS')
            estudante.media_humanas = sum(n.nota_global for n in notas_humanas) / len(notas_humanas) if notas_humanas else 0
        elif self.area == 'LINGUAGENS':
            notas_linguagens = Nota.objects.filter(estudante=estudante, area='LINGUAGENS')
            estudante.media_linguagens = sum(n.nota_global for n in notas_linguagens) / len(notas_linguagens) if notas_linguagens else 0
        elif self.area == 'EXATAS':
            notas_exatas = Nota.objects.filter(estudante=estudante, area='EXATAS')
            estudante.media_exatas = sum(n.nota_global for n in notas_exatas) / len(notas_exatas) if notas_exatas else 0
        estudante.save()

class Falta(models.Model):
    estudante = models.ForeignKey(Estudante, on_delete=models.CASCADE, related_name='faltas')
    data = models.DateField()
    aula = models.CharField(max_length=100)
    justificativa = models.TextField(blank=True, null=True)
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.estudante} - {self.data} - {self.aula}"

class ConfiguracaoLiderancaTurma(models.Model):
    """
    Configuração de liderança da turma - define quantos líderes podem existir
    """
    turma = models.OneToOneField(Turma, on_delete=models.CASCADE, related_name='config_lideranca')
    escola = models.ForeignKey('escola.Escola', on_delete=models.CASCADE, related_name='configs_lideranca')
    
    # Configurações de quantidade de líderes por cargo
    max_representantes = models.PositiveIntegerField(default=1, help_text="Máximo de representantes de turma")
    max_vice_representantes = models.PositiveIntegerField(default=1)
    max_monitores = models.PositiveIntegerField(default=2)
    max_secretarios = models.PositiveIntegerField(default=1)
    max_tesoureiros = models.PositiveIntegerField(default=1)
    
    # Permite cargos customizados
    permitir_cargos_customizados = models.BooleanField(default=True)
    
    # Configurações gerais
    duracao_mandato_meses = models.PositiveIntegerField(default=12, help_text="Duração do mandato em meses")
    
    data_criacao = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    class Meta:
        verbose_name = "Configuração de Liderança"
        verbose_name_plural = "Configurações de Liderança"

    def __str__(self):
        return f"Config Liderança - {self.turma}"
    
    def get_max_por_cargo(self, cargo):
        """Retorna o máximo permitido para um cargo"""
        mapping = {
            'REPRESENTANTE': self.max_representantes,
            'VICE_REPRESENTANTE': self.max_vice_representantes,
            'MONITOR': self.max_monitores,
            'SECRETARIO': self.max_secretarios,
            'TESOUREIRO': self.max_tesoureiros,
        }
        return mapping.get(cargo, 1)


class LiderSala(models.Model):
    estudante = models.ForeignKey(Estudante, on_delete=models.CASCADE, related_name='liderancas')
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, related_name='lideres')
    cargo = models.CharField(max_length=100, choices=[
        ('MONITOR', 'Monitor'),
        ('REPRESENTANTE', 'Representante de Turma'),
        ('VICE_REPRESENTANTE', 'Vice-Representante'),
        ('SECRETARIO', 'Secretário'),
        ('TESOUREIRO', 'Tesoureiro'),
        ('CUSTOMIZADO', 'Cargo Customizado')
    ])
    cargo_customizado = models.CharField(max_length=100, blank=True, null=True)
    data_nomeacao = models.DateTimeField(auto_now_add=True)
    data_fim_mandato = models.DateTimeField(null=True, blank=True, help_text="Data prevista de fim do mandato")
    ativo = models.BooleanField(default=True)
    responsabilidades = models.JSONField(default=list, blank=True)
    
    # Campos adicionais para controle
    pode_registrar_frequencia = models.BooleanField(default=True)
    pode_atribuir_tarefas = models.BooleanField(default=False)
    pode_fazer_observacoes = models.BooleanField(default=True)
    
    history = HistoricalRecords()

    class Meta:
        unique_together = ('estudante', 'turma', 'cargo')
        ordering = ['-data_nomeacao']
        verbose_name = "Líder de Sala"
        verbose_name_plural = "Líderes de Sala"

    def __str__(self):
        cargo_display = self.cargo_customizado if self.cargo == 'CUSTOMIZADO' else self.get_cargo_display()
        return f"{self.estudante.usuario.nome} - {cargo_display}"
    
    def nomear(self):
        """Ativa o lider e atualiza status do estudante"""
        self.ativo = True
        self.estudante.eh_lider = True
        self.estudante.cargo_lideranca = self.cargo
        self.estudante.save()
        self.save()
    
    def encerrar_mandato(self):
        """Encerra o mandato do líder"""
        self.ativo = False
        self.data_fim_mandato = models.DateTimeField(auto_now=True)
        
        # Remove status de líder se não tiver outros cargos ativos
        if not self.estudante.liderancas.filter(ativo=True).exclude(pk=self.pk).exists():
            self.estudante.eh_lider = False
            self.estudante.cargo_lideranca = None
            self.estudante.save()
        
        self.save()

class Frequencia(models.Model):
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, related_name='frequencias')
    data = models.DateField()
    aula = models.CharField(max_length=100)
    registrado_por = models.ForeignKey(Estudante, on_delete=models.CASCADE, related_name='frequencias_registradas')
    estudantes_presentes = models.ManyToManyField(Estudante, related_name='presencas', blank=True)
    estudantes_faltantes = models.ManyToManyField(Estudante, related_name='faltas_registradas', blank=True)
    observacoes = models.TextField(blank=True, null=True)
    history = HistoricalRecords()

    class Meta:
        unique_together = ('turma', 'data', 'aula')
        ordering = ['-data']

    def __str__(self):
        return f"{self.turma} - {self.data} - {self.aula}"

class ConfiguracaoEscola(models.Model):
    escola = models.ForeignKey('escola.Escola', on_delete=models.CASCADE, related_name='configuracoes')
    campo_nome = models.CharField(max_length=100)
    campo_tipo = models.CharField(max_length=20, choices=[
        ('TEXTO', 'Texto'),
        ('NUMERO', 'Número'),
        ('BOOLEANO', 'Sim/Não'),
        ('OPCOES', 'Opções Múltiplas')
    ])
    campo_opcoes = models.JSONField(default=list, blank=True)
    obrigatorio = models.BooleanField(default=False)
    ativo = models.BooleanField(default=True)
    history = HistoricalRecords()

    class Meta:
        unique_together = ('escola', 'campo_nome')

    def __str__(self):
        return f"{self.escola} - {self.campo_nome}"


# ========== NOVOS MODELOS PARA DOTs AVANÇADOS ==========

class ConfiguracaoDOT(models.Model):
    """
    Configuração geral de DoTs criada por professores ou coordenação
    Exemplo: Configuração da biblioteca para rastrear leituras
    """
    TIPO_CHOICES = [
        ('BIBLIOTECA', 'Biblioteca'),
        ('LABORATORIO', 'Laboratório'),
        ('EDUCACAO_FISICA', 'Educação Física'),
        ('ARTE', 'Arte'),
        ('BIBLOTECA_AULA', 'Biblioteca de Aula'),
        ('CUSTOMIZADO', 'Customizado')
    ]
    
    professor = models.ForeignKey('professores.Professor', on_delete=models.CASCADE, related_name='configuracoes_dot')
    escola = models.ForeignKey('escola.Escola', on_delete=models.CASCADE, related_name='configuracoes_dot')
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, related_name='configuracoes_dot', null=True, blank=True)
    
    titulo = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    tipo = models.CharField(max_length=50, choices=TIPO_CHOICES)
    
    # Campos personalizados que serão rastreados
    campos_rastreamento = models.JSONField(default=dict, blank=True, help_text="Ex: {'livros_lidos': 'number', 'tempo_estudo': 'number'}")
    
    # Configurações de pontuação
    calcular_pontos = models.BooleanField(default=True)
    pontos_por_atividade = models.IntegerField(default=1)
    criterios_pontuacao = models.JSONField(default=dict, blank=True)
    
    ativo = models.BooleanField(default=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    history = HistoricalRecords()

    class Meta:
        ordering = ['-data_criacao']
        verbose_name = "Configuração de DoT"
        verbose_name_plural = "Configurações de DoTs"

    def __str__(self):
        return f"{self.titulo} - {self.professor.usuario.nome}"


class TarefaDot(models.Model):
    """
    Tarefas específicas atribuídas a alunos com DoTs
    """
    STATUS_CHOICES = [
        ('PENDENTE', 'Pendente'),
        ('EM_ANDAMENTO', 'Em Andamento'),
        ('CONCLUIDA', 'Concluída'),
        ('CANCELADA', 'Cancelada')
    ]
    
    PRIORIDADE_CHOICES = [
        ('BAIXA', 'Baixa'),
        ('MEDIA', 'Média'),
        ('ALTA', 'Alta'),
        ('URGENTE', 'Urgente')
    ]
    
    estudante = models.ForeignKey(Estudante, on_delete=models.CASCADE, related_name='tarefas_dot')
    configuracao = models.ForeignKey(ConfiguracaoDOT, on_delete=models.CASCADE, related_name='tarefas')
    professor = models.ForeignKey('professores.Professor', on_delete=models.CASCADE, related_name='tarefas_attribuidas')
    
    titulo = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDENTE')
    prioridade = models.CharField(max_length=20, choices=PRIORIDADE_CHOICES, default='MEDIA')
    
    # Datas
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_vencimento = models.DateTimeField(null=True, blank=True)
    data_conclusao = models.DateTimeField(null=True, blank=True)
    
    # Pontuação
    pontos_obtidos = models.IntegerField(default=0)
    pontos_maximos = models.IntegerField(default=0)
    
    # Dados customizados
    dados_customizados = models.JSONField(default=dict, blank=True)
    
    observacoes = models.TextField(blank=True)
    history = HistoricalRecords()

    class Meta:
        ordering = ['-data_criacao']
        verbose_name = "Tarefa DoT"
        verbose_name_plural = "Tarefas DoTs"

    def __str__(self):
        return f"{self.titulo} - {self.estudante.usuario.nome}"

    def concluir(self, pontos=0):
        """Marca tarefa como concluída e atualiza pontos"""
        self.status = 'CONCLUIDA'
        self.data_conclusao = models.DateTimeField(auto_now=True)
        self.pontos_obtidos = pontos
        self.save()
        
        # Atualiza DoTs do estudante
        if pontos > 0:
            categoria = f"tarefas_{self.configuracao.tipo.lower()}"
            self.estudante.atualizar_dots(categoria, pontos)


class ObservacaoDot(models.Model):
    """
    Observações específicas sobre alunos com dados de DoTs
    """
    estudante = models.ForeignKey(Estudante, on_delete=models.CASCADE, related_name='observacoes_dot')
    configuracao = models.ForeignKey(ConfiguracaoDOT, on_delete=models.CASCADE, related_name='observacoes', null=True, blank=True)
    professor = models.ForeignKey('professores.Professor', on_delete=models.CASCADE, related_name='observacoes_criadas')
    
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    
    # Dados quantitativos
    dados_quantitativos = models.JSONField(default=dict, blank=True, help_text="Ex: {'livros_lidos': 5, 'horas_estudo': 10}")
    
    # Anexos
    anexo_url = models.URLField(blank=True, null=True)
    
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_observacao = models.DateTimeField()
    
    privada = models.BooleanField(default=False, help_text="Se True, só o professor vê")
    history = HistoricalRecords()

    class Meta:
        ordering = ['-data_observacao']
        verbose_name = "Observação DoT"
        verbose_name_plural = "Observações DoTs"

    def __str__(self):
        return f"{self.titulo} - {self.estudante.usuario.nome}"


class RelatorioDot(models.Model):
    """
    Relatórios gerados a partir dos DoTs dos alunos
    Ex: Relatório de leitura da biblioteca, relatório de desempenho, etc.
    """
    TIPO_CHOICES = [
        ('INDIVIDUAL', 'Individual'),
        ('TURMA', 'Turma Completa'),
        ('COMPARATIVO', 'Comparativo'),
        ('TENDENCIA', 'Tendência Temporal')
    ]
    
    configuracao = models.ForeignKey(ConfiguracaoDOT, on_delete=models.CASCADE, related_name='relatorios', null=True, blank=True)
    professor = models.ForeignKey('professores.Professor', on_delete=models.CASCADE, related_name='relatorios_criados')
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, related_name='relatorios_dot', null=True, blank=True)
    estudante = models.ForeignKey(Estudante, on_delete=models.CASCADE, related_name='relatorios_dot', null=True, blank=True)
    
    titulo = models.CharField(max_length=200)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    
    # Dados do relatório
    dados = models.JSONField(default=dict)
    
    # Filtros aplicados
    filtros_aplicados = models.JSONField(default=dict, blank=True)
    
    # Período
    data_inicio = models.DateField(null=True, blank=True)
    data_fim = models.DateField(null=True, blank=True)
    
    data_geracao = models.DateTimeField(auto_now_add=True)
    
    history = HistoricalRecords()

    class Meta:
        ordering = ['-data_geracao']
        verbose_name = "Relatório DoT"
        verbose_name_plural = "Relatórios DoTs"

    def __str__(self):
        return f"{self.titulo} - {self.data_geracao.strftime('%d/%m/%Y')}"