// types/classroom.ts

export enum TipoSala {
  NORMAL = 'NORMAL',
  LABORATORIO = 'LABORATORIO',
  BIBLIOTECA = 'BIBLIOTECA',
  AUDITORIO = 'AUDITORIO',
  CUSTOMIZADO = 'CUSTOMIZADO'
}

export enum TipoObjeto {
  CADEIRA_PROFESSOR = 'cadeira_professor',
  MESA_PROFESSOR = 'mesa_professor',
  ARMARIO = 'armario',
  COMPUTADOR = 'computador',
  ESTANTE = 'estante',
  QUADRO = 'quadro',
  CUSTOM = 'custom'
}

export interface LayoutConfig {
  espacamento_horizontal: number
  espacamento_vertical: number
  largura_assento: number
  altura_assento: number
}

export interface ObjetoSala {
  id: string
  tipo: TipoObjeto | string
  x: number
  y: number
  width: number
  height: number
  rotacao: number
  label: string
  cor: string
  selected?: boolean
}

export interface Estudante {
  id: number
  usuario: {
    id: string
    nome: string
    email?: string
  }
  turma: {
    id: number
    nome: string
  }
  dificuldade_visao?: string
  dificuldade_aprendizado?: string
  altura?: string
  media_humanas?: number
  media_linguagens?: number
  media_exatas?: number
  eh_lider?: boolean
}

export interface PosicaoAluno {
  id?: number
  estudante_id: number
  estudante?: Estudante
  linha: number
  coluna: number
  numero_grupo: number | null
  posicao_no_grupo: number
  fixo?: boolean
  eh_lider?: boolean
  observacoes?: string
  posicionado_em?: string
  atualizado_em?: string
}

export interface MapeamentoConfig {
  uuid?: string
  turma_id: number
  nome: string
  fileiras_verticais: number
  fileiras_horizontais: number
  alunos_por_grupo: number
  tipo_sala: TipoSala
  layout_config?: LayoutConfig
  objetos_sala?: ObjetoSala[]
  cor_fundo?: string
  mostrar_grade?: boolean
  mostrar_numeros?: boolean
  ativo?: boolean
  usar_sistema_lideres?: boolean
  posicionamento_lideres?: any
  usar_ia_automatica?: boolean
  criterios_ia?: any
  modo_edicao?: string
  criado_em?: string
  atualizado_em?: string
  turma?: any
  escola?: any
}

export interface TemplateSala {
  id: number
  nome: string
  tipo_sala: TipoSala
  descricao: string
  config: MapeamentoConfig
  publico: boolean
  criado_em?: string
  atualizado_em?: string
}

export interface AlunoMapeamentoResponse {
  mapeamento: MapeamentoConfig
  posicoes: PosicaoAluno[]
  sua_posicao: PosicaoAluno | null
  seu_id: number
}
