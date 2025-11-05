// services/classroomApi.ts
import { apiService } from './api'
import type { 
  MapeamentoConfig, 
  PosicaoAluno, 
  ObjetoSala, 
  TemplateSala,
  AlunoMapeamentoResponse,
  Estudante
} from '@/types/classroom'

const API_URL = '/api/mapeamento'

export const classroomApi = {
  // === DEMONSTRAÇÃO ===
  async getTemplates(): Promise<TemplateSala[]> {
    const { data } = await apiService.get<TemplateSala[]>(`${API_URL}/demo/templates/`)
    return data
  },

  async getTemplate(id: number): Promise<TemplateSala> {
    const { data } = await apiService.get<TemplateSala>(`${API_URL}/demo/template/${id}/`)
    return data
  },

  // === ALUNO ===
  async getMapeamentoAluno(): Promise<AlunoMapeamentoResponse> {
    const { data } = await apiService.get<AlunoMapeamentoResponse>(`${API_URL}/aluno/mapeamento-atual/`)
    return data
  },

  // === PROFESSOR ===
  async getMapeamentos(turmaId?: number): Promise<MapeamentoConfig[]> {
    const params = turmaId ? { params: { turma_id: turmaId } } : undefined
    const { data } = await apiService.get<MapeamentoConfig[]>(`${API_URL}/professor/mapeamentos/`, params)
    return data
  },

  async getMapeamento(uuid: string): Promise<{ mapeamento: MapeamentoConfig; posicoes: PosicaoAluno[] }> {
    const { data } = await apiService.get<{ mapeamento: MapeamentoConfig; posicoes: PosicaoAluno[] }>(
      `${API_URL}/professor/mapeamento/${uuid}/`
    )
    return data
  },

  async criarMapeamento(config: Partial<MapeamentoConfig>): Promise<MapeamentoConfig> {
    const { data } = await apiService.post<MapeamentoConfig>(`${API_URL}/professor/mapeamento/criar/`, config)
    return data
  },

  async atualizarMapeamento(uuid: string, config: Partial<MapeamentoConfig>): Promise<MapeamentoConfig> {
    const { data } = await apiService.patch<MapeamentoConfig>(
      `${API_URL}/professor/mapeamento/${uuid}/`,
      config
    )
    return data
  },

  async deletarMapeamento(uuid: string): Promise<void> {
    await apiService.delete(`${API_URL}/professor/mapeamento/${uuid}/`)
  },

  async atualizarPosicoes(uuid: string, posicoes: PosicaoAluno[]): Promise<{ message: string; total: number; posicoes: PosicaoAluno[] }> {
    const { data } = await apiService.patch<{ message: string; total: number; posicoes: PosicaoAluno[] }>(
      `${API_URL}/professor/mapeamento/${uuid}/posicoes/`,
      { posicoes }
    )
    return data
  },

  async atualizarObjetos(uuid: string, objetos: ObjetoSala[]): Promise<{ message: string; objetos: ObjetoSala[] }> {
    const { data } = await apiService.put<{ message: string; objetos: ObjetoSala[] }>(
      `${API_URL}/professor/mapeamento/${uuid}/objetos/`,
      { objetos }
    )
    return data
  },

  async organizarAutomatico(uuid: string, criterios?: any): Promise<{ message: string; posicoes: PosicaoAluno[]; total: number }> {
    const { data } = await apiService.post<{ message: string; posicoes: PosicaoAluno[]; total: number }>(
      `${API_URL}/professor/mapeamento/${uuid}/organizar-automatico/`,
      criterios || {}
    )
    return data
  },

  async getTemplatesSala(): Promise<TemplateSala[]> {
    const { data } = await apiService.get<TemplateSala[]>(`${API_URL}/professor/templates-sala/`)
    return data
  },

  // === ESTUDANTES ===
  async getEstudantes(turmaId: number): Promise<Estudante[]> {
    const { data } = await apiService.get<Estudante[]>(`/api/estudantes/`, {
      params: { turma_id: turmaId }
    })
    return data
  }
}

