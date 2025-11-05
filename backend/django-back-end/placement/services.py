# placement/services.py
"""
Serviços avançados de organização de salas de aula com IA
Implementa algoritmos sofisticados para otimização de layouts
"""
from typing import List, Dict, Any, Tuple
from django.db.models import Q, F
from collections import defaultdict
import random
from estudantes.models import Estudante
import logging

logger = logging.getLogger(__name__)


class IAMapeamentoSala:
    """
    Serviço de IA para organização inteligente de salas de aula
    """
    
    def __init__(self, mapeamento):
        from .models import MapeamentoSala
        self.mapeamento = mapeamento
        self.turma = mapeamento.turma
        self.criterios = mapeamento.criterios_ia or {}
        # Usar novos campos se disponíveis, senão usar legados
        self.linhas = mapeamento.fileiras_verticais or mapeamento.linhas or 5
        self.colunas = mapeamento.fileiras_horizontais or mapeamento.colunas or 6
        self.alunos_por_grupo = mapeamento.alunos_por_grupo or mapeamento.numero_pessoas_grupo or 1
        self.tipo_agrupamento = mapeamento.tipo_agrupamento or 'SOLO'
        self.numero_pessoas_grupo = mapeamento.alunos_por_grupo or mapeamento.numero_pessoas_grupo or 1
        
    def organizar_automaticamente(self) -> List[Dict[str, Any]]:
        """
        Organiza automaticamente a sala de aula usando IA
        Retorna lista de posições sugeridas
        """
        logger.info(f"Organizando sala {self.mapeamento.nome} com IA")
        
        # Obter todos os estudantes da turma
        estudantes = list(Estudante.objects.filter(turma=self.turma))
        
        if not estudantes:
            logger.warning("Nenhum estudante encontrado na turma")
            return []
        
        # Aplicar critérios de organização
        if self.criterios.get('considerar_dificuldades', True):
            return self._organizar_por_dificuldades(estudantes)
        elif self.criterios.get('considerar_notas', False):
            return self._organizar_por_desempenho(estudantes)
        elif self.criterios.get('considerar_altura', False):
            return self._organizar_por_altura(estudantes)
        elif self.criterios.get('considerar_lideranca', False):
            return self._organizar_com_lideres(estudantes)
        else:
            return self._organizar_hibrido(estudantes)
    
    def _organizar_por_dificuldades(self, estudantes: List[Estudante]) -> List[Dict[str, Any]]:
        """
        Organiza considerando dificuldades de aprendizado e visão
        Algoritmo: Pares heterogêneos (aluno com dificuldade + aluno sem dificuldade)
        """
        logger.info("Organizando por dificuldades")
        
        # Separar estudantes por dificuldades
        com_dificuldade = []
        sem_dificuldade = []
        
        for estudante in estudantes:
            tem_dificuldade = (
                estudante.dificuldade_aprendizado in ['MODERADA', 'SEVERA'] or
                estudante.dificuldade_visao in ['MEDIA', 'ALTA']
            )
            
            if tem_dificuldade:
                com_dificuldade.append(estudante)
            else:
                sem_dificuldade.append(estudante)
        
        # Organizar em pares heterogêneos
        posicoes = []
        posicao = 0
        
        # Emparelhar estudantes com e sem dificuldade
        pares = min(len(com_dificuldade), len(sem_dificuldade))
        
        for i in range(pares):
            linha, coluna = self._calcular_posicao(posicao)
            posicoes.append({
                'estudante': com_dificuldade[i],
                'linha': linha,
                'coluna': coluna,
                'grupo': i
            })
            
            posicao += 1
            linha, coluna = self._calcular_posicao(posicao)
            posicoes.append({
                'estudante': sem_dificuldade[i],
                'linha': linha,
                'coluna': coluna,
                'grupo': i
            })
            posicao += 1
        
        # Adicionar estudantes restantes
        estudantes_restantes = com_dificuldade[pares:] + sem_dificuldade[pares:]
        for estudante in estudantes_restantes:
            linha, coluna = self._calcular_posicao(posicao)
            posicoes.append({
                'estudante': estudante,
                'linha': linha,
                'coluna': coluna,
                'grupo': posicao
            })
            posicao += 1
        
        return posicoes
    
    def _organizar_por_desempenho(self, estudantes: List[Estudante]) -> List[Dict[str, Any]]:
        """
        Organiza por desempenho acadêmico
        Algoritmo: Distribui alunos com notas altas e baixas uniformemente
        """
        logger.info("Organizando por desempenho")
        
        # Ordenar por média geral
        estudantes_ordenados = sorted(
            estudantes,
            key=lambda e: (e.media_humanas + e.media_linguagens + e.media_exatas) / 3,
            reverse=True
        )
        
        posicoes = []
        # Técnica de distribuição: colocar melhores no meio, demais nas bordas
        meio_linha = self.linhas // 2
        meio_coluna = self.colunas // 2
        
        for i, estudante in enumerate(estudantes_ordenados):
            linha, coluna = self._calcular_posicao_distribuida(
                i, len(estudantes_ordenados), meio_linha, meio_coluna
            )
            posicoes.append({
                'estudante': estudante,
                'linha': linha,
                'coluna': coluna,
                'grupo': i // self.numero_pessoas_grupo
            })
        
        return posicoes
    
    def _organizar_por_altura(self, estudantes: List[Estudante]) -> List[Dict[str, Any]]:
        """
        Organiza por altura (baixos na frente, altos atrás)
        """
        logger.info("Organizando por altura")
        
        # Ordenar por altura (BAIXA -> MEDIA -> ALTA)
        ordem_altura = {'BAIXA': 0, 'MEDIA': 1, 'ALTA': 2}
        estudantes_ordenados = sorted(
            estudantes,
            key=lambda e: ordem_altura.get(e.altura, 1)
        )
        
        posicoes = []
        for i, estudante in enumerate(estudantes_ordenados):
            linha, coluna = self._calcular_posicao(i)
            posicoes.append({
                'estudante': estudante,
                'linha': linha,
                'coluna': coluna,
                'grupo': 0
            })
        
        return posicoes
    
    def _organizar_com_lideres(self, estudantes: List[Estudante]) -> List[Dict[str, Any]]:
        """
        Organiza com líderes estrategicamente posicionados
        """
        logger.info("Organizando com líderes estratégicos")
        
        # Separar líderes
        lideres = [e for e in estudantes if e.eh_lider]
        nao_lideres = [e for e in estudantes if not e.eh_lider]
        
        posicoes = []
        posicao = 0
        
        # Posicionar líderes estrategicamente (primeira e última linha)
        posicoes_lider = [0, self.linhas - 1]
        
        for i, lider in enumerate(lideres):
            linha = posicoes_lider[i % len(posicoes_lider)]
            coluna = i % self.colunas
            posicoes.append({
                'estudante': lider,
                'linha': linha,
                'coluna': coluna,
                'grupo': 'lider',
                'eh_lider': True
            })
            posicao += 1
        
        # Preencher posições restantes com não-líderes
        for estudante in nao_lideres:
            linha, coluna = self._calcular_posicao(posicao)
            # Garantir que não vai para posição já ocupada por líder
            while any(p['linha'] == linha and p['coluna'] == coluna for p in posicoes):
                linha, coluna = self._calcular_posicao(posicao + 1)
                posicao += 1
            
            posicoes.append({
                'estudante': estudante,
                'linha': linha,
                'coluna': coluna,
                'grupo': posicao // self.numero_pessoas_grupo
            })
            posicao += 1
        
        return posicoes
    
    def _organizar_hibrido(self, estudantes: List[Estudante]) -> List[Dict[str, Any]]:
        """
        Algoritmo híbrido que combina múltiplos critérios
        """
        logger.info("Organizando com algoritmo híbrido")
        
        # Calcular score para cada estudante
        estudantes_com_score = []
        
        for estudante in estudantes:
            score = 0
            
            # Dificuldades aumentam prioridade para frente
            if estudante.dificuldade_visao in ['MEDIA', 'ALTA']:
                score += 100
            if estudante.dificuldade_aprendizado in ['MODERADA', 'SEVERA']:
                score += 50
            
            # Altura baixa aumenta prioridade para frente
            if estudante.altura == 'BAIXA':
                score += 30
            
            # Líderes vão para posições estratégicas
            if estudante.eh_lider:
                score += 200
            
            # Desempenho médio também é considerado
            media_geral = (estudante.media_humanas + estudante.media_linguagens + estudante.media_exatas) / 3
            score += media_geral
            
            estudantes_com_score.append({
                'estudante': estudante,
                'score': score
            })
        
        # Ordenar por score (maior -> menor)
        estudantes_com_score.sort(key=lambda x: x['score'], reverse=True)
        
        posicoes = []
        posicoes_ocupadas = set()
        
        for idx, item in enumerate(estudantes_com_score):
            estudante = item['estudante']
            
            # Calcular posição ideal
            if estudante.eh_lider:
                # Líderes vão para cantos ou laterais
                linha = 0 if idx < len(estudantes_com_score) / 2 else self.linhas - 1
                coluna = (idx * 2) % self.colunas
            elif item['score'] > 150:
                # Alta prioridade - frente da sala
                linha = idx % min(2, self.linhas)
                coluna = (idx // 2) % self.colunas
            else:
                # Posição padrão
                linha, coluna = self._calcular_posicao(idx)
            
            # Garantir que não há conflito
            tentativas = 0
            while (linha, coluna) in posicoes_ocupadas and tentativas < self.linhas * self.colunas:
                linha, coluna = self._calcular_posicao(idx + tentativas)
                tentativas += 1
            
            posicoes_ocupadas.add((linha, coluna))
            
            posicoes.append({
                'estudante': estudante,
                'linha': linha,
                'coluna': coluna,
                'grupo': idx // self.numero_pessoas_grupo,
                'eh_lider': estudante.eh_lider
            })
        
        return posicoes
    
    def _calcular_posicao(self, indice: int) -> Tuple[int, int]:
        """Calcula posição baseada no índice sequencial"""
        linha = indice // self.colunas
        coluna = indice % self.colunas
        # Garantir que não excede os limites
        linha = min(linha, self.linhas - 1)
        coluna = min(coluna, self.colunas - 1)
        return linha, coluna
    
    def _calcular_posicao_distribuida(self, indice: int, total: int, meio_linha: int, meio_coluna: int) -> Tuple[int, int]:
        """Calcula posição distribuída uniformemente na sala"""
        # Espiral do centro para fora
        distancia = abs(indice - total // 2)
        linha = max(0, min(meio_linha + (indice % 3) - 1, self.linhas - 1))
        coluna = max(0, min(meio_coluna + (indice % 3) - 1, self.colunas - 1))
        return linha, coluna
    
    def analisar_layout_otimo(self) -> Dict[str, Any]:
        """
        Analisa e sugere melhor layout baseado nas características dos alunos
        """
        estudantes = list(Estudante.objects.filter(turma=self.turma))
        
        analise = {
            'total_alunos': len(estudantes),
            'alunos_dificuldade': len([e for e in estudantes if e.dificuldade_aprendizado in ['MODERADA', 'SEVERA']]),
            'alunos_visao': len([e for e in estudantes if e.dificuldade_visao in ['MEDIA', 'ALTA']]),
            'lideres': len([e for e in estudantes if e.eh_lider]),
            'sugestao_agrupamento': self._sugerir_agrupamento(len(estudantes)),
            'prioridades_posicionamento': []
        }
        
        # Sugerir prioridades
        if analise['alunos_dificuldade'] > 0:
            analise['prioridades_posicionamento'].append('ALUNOS_ACESSO_FACIL')
        if analise['alunos_visao'] > 0:
            analise['prioridades_posicionamento'].append('ALUNOS_FRENTE_QUADRO')
        if analise['lideres'] > 0:
            analise['prioridades_posicionamento'].append('LIDERES_ESTRATEGICOS')
        
        return analise
    
    def _sugerir_agrupamento(self, total_alunos: int) -> str:
        """Sugere melhor tipo de agrupamento"""
        if total_alunos <= 12:
            return 'DUPLA'
        elif total_alunos <= 24:
            return 'TRIO'
        elif total_alunos <= 30:
            return 'QUARTETO'
        else:
            return 'SOLO'


class OtimizadorMapeamento:
    """
    Otimizador avançado para melhorar layouts existentes
    """
    
    @staticmethod
    def otimizar_posicionamento(mapeamento, iteracoes: int = 100) -> List[Dict[str, Any]]:
        """
        Otimiza posicionamento usando algoritmos genéticos
        """
        from .models import PosicaoAluno
        logger.info(f"Otimizando mapeamento {mapeamento.nome}")
        
        # Obter posições atuais
        posicoes = list(PosicaoAluno.objects.filter(mapeamento=mapeamento))
        
        melhor_score = OtimizadorMapeamento._calcular_score(posicoes)
        melhor_layout = posicoes.copy()
        
        for _ in range(iteracoes):
            # Criar variação do layout
            layout_teste = OtimizadorMapeamento._mutar_layout(posicoes)
            score = OtimizadorMapeamento._calcular_score(layout_teste)
            
            if score > melhor_score:
                melhor_score = score
                melhor_layout = layout_teste
        
        return melhor_layout
    
    @staticmethod
    def _calcular_score(posicoes) -> float:
        """
        Calcula score de qualidade do layout
        """
        score = 0.0
        
        for pos in posicoes:
            estudante = pos.estudante
            
            # Penalizar alunos com dificuldade visual longe do quadro
            if estudante.dificuldade_visao in ['MEDIA', 'ALTA']:
                if pos.linha > 3:
                    score -= 10
            
            # Bonificar líderes em posições estratégicas (lados da sala)
            if estudante.eh_lider:
                if pos.coluna in [0, pos.mapeamento.colunas - 1]:
                    score += 5
            
            # Penalizar muito perto ou muito longe
            if pos.linha == 0 or pos.linha == pos.mapeamento.linhas - 1:
                score -= 2
        
        return score
    
    @staticmethod
    def _mutar_layout(posicoes) -> List:
        """
        Cria variação do layout trocando duas posições aleatoriamente
        """
        import copy
        layout_novo = copy.deepcopy(posicoes)
        
        # Selecionar duas posições aleatórias para trocar
        if len(layout_novo) < 2:
            return layout_novo
        
        idx1, idx2 = random.sample(range(len(layout_novo)), 2)
        
        # Trocar posições
        layout_novo[idx1].linha, layout_novo[idx2].linha = layout_novo[idx2].linha, layout_novo[idx1].linha
        layout_novo[idx1].coluna, layout_novo[idx2].coluna = layout_novo[idx2].coluna, layout_novo[idx1].coluna
        
        return layout_novo


class ValidacaoMapeamento:
    """
    Validações avançadas para mapeamento de sala
    """
    
    @staticmethod
    def validar_layout(mapeamento) -> Dict[str, Any]:
        """
        Valida o layout e retorna problemas encontrados
        """
        from .models import PosicaoAluno
        problemas = []
        avisos = []
        
        # Obter posições
        posicoes = PosicaoAluno.objects.filter(mapeamento=mapeamento)
        
        # Verificar capacidade
        capacidade_total = mapeamento.linhas * mapeamento.colunas
        if posicoes.count() > capacidade_total:
            problemas.append({
                'tipo': 'CAPACIDADE_EXCEDIDA',
                'mensagem': f'Tem {posicoes.count()} alunos mas capacidade é {capacidade_total}',
                'severidade': 'ERRO'
            })
        
        # Verificar alunos com dificuldade visual longe
        for pos in posicoes:
            estudante = pos.estudante
            
            if estudante.dificuldade_visao in ['MEDIA', 'ALTA'] and pos.linha > 3:
                avisos.append({
                    'tipo': 'VISAO_LONGE',
                    'mensagem': f'{estudante.usuario.nome} com dificuldade visual está longe do quadro',
                    'severidade': 'AVISO'
                })
            
            # Verificar altura
            if estudante.altura == 'BAIXA' and pos.linha > 2:
                avisos.append({
                    'tipo': 'ALTURA_ATRAS',
                    'mensagem': f'{estudante.usuario.nome} de altura baixa está atrás',
                    'severidade': 'AVISO'
                })
        
        return {
            'valido': len(problemas) == 0,
            'problemas': problemas,
            'avisos': avisos
        }


class EstatisticasMapeamento:
    """
    Gera estatísticas e análises do mapeamento
    """
    
    @staticmethod
    def gerar_estatisticas(mapeamento) -> Dict[str, Any]:
        """
        Gera estatísticas detalhadas do mapeamento
        """
        from .models import PosicaoAluno
        posicoes = PosicaoAluno.objects.filter(mapeamento=mapeamento).select_related('estudante')
        
        stats = {
            'total_alunos': posicoes.count(),
            'distribuicao_altura': defaultdict(int),
            'distribuicao_dificuldades': defaultdict(int),
            'lideres_posicionados': 0,
            'taxa_ocupacao': 0,
            'densidade_por_setor': {}
        }
        
        for pos in posicoes:
            estudante = pos.estudante
            
            # Distribuição por altura
            stats['distribuicao_altura'][estudante.altura] += 1
            
            # Distribuição por dificuldades
            if estudante.dificuldade_aprendizado != 'NENHUMA':
                stats['distribuicao_dificuldades']['aprendizado'] += 1
            if estudante.dificuldade_visao != 'NENHUMA':
                stats['distribuicao_dificuldades']['visao'] += 1
            
            # Líderes
            if estudante.eh_lider:
                stats['lideres_posicionados'] += 1
        
        # Taxa de ocupação
        capacidade = mapeamento.linhas * mapeamento.colunas
        stats['taxa_ocupacao'] = (stats['total_alunos'] / capacidade * 100) if capacidade > 0 else 0
        
        return stats


def gerar_novo_mapeamento(turma, escola, nome="Mapeamento Automático", linhas=4, colunas=5):
    """
    Função principal para gerar um novo mapeamento de sala
    """
    from .models import MapeamentoSala, PosicaoAluno
    from escola.models import Turma
    
    # Criar o mapeamento
    mapeamento = MapeamentoSala.objects.create(
        nome=nome,
        turma=turma,
        escola=escola,
        linhas=linhas,
        colunas=colunas,
        tipo_agrupamento='DUPLA',
        numero_pessoas_grupo=2,
        criterios_ia={
            'considerar_dificuldades': True,
            'considerar_notas': False,
            'considerar_altura': True,
            'considerar_lideranca': True
        }
    )
    
    # Usar IA para organizar
    ia_service = IAMapeamentoSala(mapeamento)
    posicoes_sugeridas = ia_service.organizar_automaticamente()
    
    # Criar posições dos alunos
    for posicao_data in posicoes_sugeridas:
        PosicaoAluno.objects.create(
            mapeamento=mapeamento,
            estudante=posicao_data['estudante'],
            linha=posicao_data['linha'],
            coluna=posicao_data['coluna'],
            grupo=posicao_data.get('grupo', 0)
        )
    
    return mapeamento