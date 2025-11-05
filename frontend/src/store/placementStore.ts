// store/placementStore.ts
import { defineStore } from 'pinia'
import { classroomApi } from '@/services/classroomApi'
import type { 
  MapeamentoConfig, 
  PosicaoAluno, 
  ObjetoSala, 
  Estudante,
  TemplateSala
} from '@/types/classroom'

export interface PlacementState {
  mapeamentoAtual: MapeamentoConfig | null
  posicoes: PosicaoAluno[]
  objetos: ObjetoSala[]
  estudantes: Estudante[]
  templates: TemplateSala[]
  loading: boolean
  error: string | null
}

export const usePlacementStore = defineStore('placement', {
  state: (): PlacementState => ({
    mapeamentoAtual: null,
    posicoes: [],
    objetos: [],
    estudantes: [],
    templates: [],
    loading: false,
    error: null
  }),

  getters: {
    estudantesPosicionados(): number[] {
      return this.posicoes.map(p => p.estudante_id)
    },

    estudantesDisponiveis(): Estudante[] {
      return this.estudantes.filter(e => !this.estudantesPosicionados.includes(e.id))
    },

    totalAssentos(): number {
      if (!this.mapeamentoAtual) return 0
      const linhas = this.mapeamentoAtual.fileiras_verticais || 5
      const colunas = this.mapeamentoAtual.fileiras_horizontais || 6
      const alunosPorGrupo = this.mapeamentoAtual.alunos_por_grupo || 1
      return linhas * colunas * alunosPorGrupo
    },

    taxaOcupacao(): number {
      if (this.totalAssentos === 0) return 0
      return (this.posicoes.length / this.totalAssentos) * 100
    },

    objetosPorTipo(): Record<string, ObjetoSala[]> {
      const agrupados: Record<string, ObjetoSala[]> = {}
      this.objetos.forEach(obj => {
        if (!agrupados[obj.tipo]) {
          agrupados[obj.tipo] = []
        }
        agrupados[obj.tipo].push(obj)
      })
      return agrupados
    }
  },

  actions: {
    async carregarMapeamento(uuid: string): Promise<boolean> {
      this.loading = true
      this.error = null
      try {
        const data = await classroomApi.getMapeamento(uuid)
        this.mapeamentoAtual = data.mapeamento
        this.posicoes = data.posicoes
        this.objetos = data.mapeamento.objetos_sala || []
        return true
      } catch (e: any) {
        this.error = e.response?.data?.error || e.message || 'Erro ao carregar mapeamento'
        console.error('Erro ao carregar mapeamento:', e)
        return false
      } finally {
        this.loading = false
      }
    },

    async carregarEstudantes(turmaId: number): Promise<boolean> {
      try {
        this.estudantes = await classroomApi.getEstudantes(turmaId)
        return true
      } catch (e: any) {
        this.error = e.response?.data?.error || e.message || 'Erro ao carregar estudantes'
        console.error('Erro ao carregar estudantes:', e)
        return false
      }
    },

    async carregarTemplates(): Promise<boolean> {
      try {
        this.templates = await classroomApi.getTemplates()
        return true
      } catch (e: any) {
        this.error = e.response?.data?.error || e.message || 'Erro ao carregar templates'
        console.error('Erro ao carregar templates:', e)
        return false
      }
    },

    async criarMapeamento(config: Partial<MapeamentoConfig>): Promise<MapeamentoConfig | null> {
      this.loading = true
      try {
        const mapeamento = await classroomApi.criarMapeamento(config)
        this.mapeamentoAtual = mapeamento
        this.posicoes = []
        this.objetos = mapeamento.objetos_sala || []
        return mapeamento
      } catch (e: any) {
        this.error = e.response?.data?.error || e.message || 'Erro ao criar mapeamento'
        console.error('Erro ao criar mapeamento:', e)
        return null
      } finally {
        this.loading = false
      }
    },

    adicionarPosicao(posicao: PosicaoAluno): void {
      // Remove se já existe nesta posição
      const index = this.posicoes.findIndex(
        p => p.linha === posicao.linha && p.coluna === posicao.coluna
      )
      if (index !== -1) {
        this.posicoes.splice(index, 1)
      }
      
      // Remove se aluno já está em outra posição
      const indexAluno = this.posicoes.findIndex(
        p => p.estudante_id === posicao.estudante_id
      )
      if (indexAluno !== -1) {
        this.posicoes.splice(indexAluno, 1)
      }
      
      this.posicoes.push(posicao)
    },

    removerPosicao(estudanteId: number): void {
      const index = this.posicoes.findIndex(p => p.estudante_id === estudanteId)
      if (index !== -1) {
        this.posicoes.splice(index, 1)
      }
    },

    atualizarPosicao(estudanteId: number, updates: Partial<PosicaoAluno>): void {
      const index = this.posicoes.findIndex(p => p.estudante_id === estudanteId)
      if (index !== -1) {
        this.posicoes[index] = { ...this.posicoes[index], ...updates }
      }
    },

    adicionarObjeto(objeto: ObjetoSala): void {
      this.objetos.push(objeto)
    },

    atualizarObjeto(id: string, updates: Partial<ObjetoSala>): void {
      const index = this.objetos.findIndex(o => o.id === id)
      if (index !== -1) {
        this.objetos[index] = { ...this.objetos[index], ...updates }
      }
    },

    removerObjeto(id: string): void {
      const index = this.objetos.findIndex(o => o.id === id)
      if (index !== -1) {
        this.objetos.splice(index, 1)
      }
    },

    async salvarMapeamento(): Promise<boolean> {
      if (!this.mapeamentoAtual?.uuid) return false
      
      this.loading = true
      this.error = null
      try {
        // Atualiza mapeamento
        await classroomApi.atualizarMapeamento(
          this.mapeamentoAtual.uuid!,
          {
            ...this.mapeamentoAtual,
            objetos_sala: this.objetos
          }
        )
        
        // Atualiza posições
        await classroomApi.atualizarPosicoes(
          this.mapeamentoAtual.uuid!,
          this.posicoes
        )
        
        // Atualiza objetos
        await classroomApi.atualizarObjetos(
          this.mapeamentoAtual.uuid!,
          this.objetos
        )
        
        return true
      } catch (e: any) {
        this.error = e.response?.data?.error || e.message || 'Erro ao salvar mapeamento'
        console.error('Erro ao salvar mapeamento:', e)
        return false
      } finally {
        this.loading = false
      }
    },

    async organizarAutomatico(criterios?: any): Promise<boolean> {
      if (!this.mapeamentoAtual?.uuid) return false
      
      this.loading = true
      this.error = null
      try {
        const result = await classroomApi.organizarAutomatico(
          this.mapeamentoAtual.uuid!,
          criterios
        )
        this.posicoes = result.posicoes
        return true
      } catch (e: any) {
        this.error = e.response?.data?.error || e.message || 'Erro ao organizar automaticamente'
        console.error('Erro ao organizar automaticamente:', e)
        return false
      } finally {
        this.loading = false
      }
    },

    limparTudo(): void {
      this.posicoes = []
      this.objetos = []
    },

    resetar(): void {
      this.mapeamentoAtual = null
      this.posicoes = []
      this.objetos = []
      this.estudantes = []
      this.templates = []
      this.error = null
    },

    clearError(): void {
      this.error = null
    }
  }
})

