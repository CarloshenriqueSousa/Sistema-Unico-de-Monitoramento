import { defineStore } from 'pinia'
import axios from 'axios'
import type {
  AIActivitySuggestion,
  AIExamSuggestion,
  AIChatMessage,
  AIAnalysisReport,
  AIUsageStats,
  AIOptimizationResult,
  AIResponse,
  AIGenerateActivityRequest,
  AIGenerateNotesRequest,
  AIGenerateExamRequest,
  AIAnalyzeDotsRequest,
  AIOptimizeClassroomRequest
} from '@/types/ai'

export interface AIState {
  responses: AIResponse[]
  generatedActivities: AIActivitySuggestion[]
  generatedNotes: string[]
  chatHistory: AIChatMessage[]
  isLoading: boolean
  error: string | null
  usage: AIUsageStats
}

export const useAIStore = defineStore('ai', {
  state: (): AIState => ({
    responses: [],
    generatedActivities: [],
    generatedNotes: [],
    chatHistory: [],
    isLoading: false,
    error: null,
    usage: {
      tokens: 0,
      requests: 0,
      lastRequest: undefined,
      averageResponseTime: 0,
      totalCost: 0
    }
  }),

  getters: {
    recentActivities: (state): AIActivitySuggestion[] =>
      state.generatedActivities.slice(-10).reverse(),
    recentNotes: (state): string[] =>
      state.generatedNotes.slice(-10).reverse(),
    recentResponses: (state): AIResponse[] =>
      state.responses.slice(-20).reverse(),
    recentChat: (state): AIChatMessage[] =>
      state.chatHistory.slice(-50),
    totalUsage: (state) => ({
      tokens: state.usage.tokens,
      requests: state.usage.requests,
      averageResponseTime: state.usage.averageResponseTime || 0,
      estimatedCost: state.usage.totalCost || 0,
      costPerRequest: state.usage.requests > 0
        ? (state.usage.totalCost || 0) / state.usage.requests
        : 0
    }),
    activitiesByDifficulty: (state) => (difficulty: string) =>
      state.generatedActivities.filter(a => a.difficulty === difficulty),
    activitiesBySubject: (state) => (subject: string) =>
      state.generatedActivities.filter(a =>
        a.subject.toLowerCase().includes(subject.toLowerCase())
      ),
    lastActivity: (state): AIActivitySuggestion | null =>
      state.generatedActivities.length > 0
        ? state.generatedActivities[state.generatedActivities.length - 1]
        : null,
    hasError: (state): boolean => state.error !== null
  },

  actions: {
    async generateActivity(request: AIGenerateActivityRequest): Promise<AIActivitySuggestion | null> {
      this.isLoading = true
      this.error = null
      const startTime = Date.now()
      try {
        const response = await axios.post<AIActivitySuggestion>(
          '/api/ai/generate-activity/',
          request
        )
        const activity: AIActivitySuggestion = {
          ...response.data,
          generatedAt: response.data.generatedAt || new Date().toISOString()
        }
        this.generatedActivities.push(activity)
        this.responses.push({
          type: 'activity',
          content: activity,
          timestamp: new Date(),
          tokensUsed: activity?.content?.length || 0,
          model: 'gpt-4-turbo'
        })
        this.updateUsage(activity?.content?.length || 0, Date.now() - startTime)
        return activity
      } catch (error: any) {
        this.error = error?.response?.data?.message || 'Falha ao gerar atividade'
        console.error('Erro ao gerar atividade:', error)
        return null
      } finally {
        this.isLoading = false
      }
    },

    async generateNotes(request: AIGenerateNotesRequest): Promise<string | null> {
      this.isLoading = true
      this.error = null
      const startTime = Date.now()
      try {
        const response = await axios.post<{ notes: string } | string>(
          '/api/ai/generate-notes/',
          request
        )
        const notes: string = typeof response.data === 'string'
          ? response.data
          : response.data.notes
        this.generatedNotes.push(notes)
        this.responses.push({
          type: 'notes',
          content: notes,
          timestamp: new Date(),
          tokensUsed: notes?.length || 0
        })
        this.updateUsage(notes?.length || 0, Date.now() - startTime)
        return notes
      } catch (error: any) {
        this.error = error?.response?.data?.message || 'Falha ao gerar anotações'
        console.error('Erro ao gerar anotações:', error)
        return null
      } finally {
        this.isLoading = false
      }
    },

    async analyzeDots(userId: number, options?: AIAnalyzeDotsRequest): Promise<AIAnalysisReport | null> {
      this.isLoading = true
      this.error = null
      const startTime = Date.now()
      try {
        const params = new URLSearchParams()
        if (options?.includeHistory) params.append('includeHistory', 'true')
        if (options?.timeFrame) params.append('timeFrame', options.timeFrame)
        const url = `/api/ai/analyze-dots/${userId}/${params.toString() ? '?' + params.toString() : ''}`
        const response = await axios.get<AIAnalysisReport>(url)
        const analysis: AIAnalysisReport = {
          ...response.data,
          generatedAt: response.data.generatedAt || new Date().toISOString()
        }
        this.responses.push({
          type: 'dots-analysis',
          content: analysis,
          timestamp: new Date(),
          tokensUsed: analysis?.summary?.length || 0
        })
        this.updateUsage(analysis?.summary?.length || 0, Date.now() - startTime)
        return analysis
      } catch (error: any) {
        this.error = error?.response?.data?.message || 'Falha na análise DOTS'
        console.error('Erro na análise DOTS:', error)
        return null
      } finally {
        this.isLoading = false
      }
    },

    async optimizeClassroom(classroomId: number, options?: AIOptimizeClassroomRequest): Promise<AIOptimizationResult | null> {
      this.isLoading = true
      this.error = null
      const startTime = Date.now()
      try {
        const response = await axios.post<AIOptimizationResult>(
          `/api/ai/optimize-classroom/${classroomId}/`,
          options || {}
        )
        const optimization: AIOptimizationResult = {
          ...response.data,
          generatedAt: response.data.generatedAt || new Date().toISOString()
        }
        this.responses.push({
          type: 'classroom-optimization',
          content: optimization,
          timestamp: new Date(),
          tokensUsed: JSON.stringify(optimization).length
        })
        this.updateUsage(JSON.stringify(optimization).length, Date.now() - startTime)
        return optimization
      } catch (error: any) {
        this.error = error?.response?.data?.message || 'Falha na otimização de sala'
        console.error('Erro na otimização:', error)
        return null
      } finally {
        this.isLoading = false
      }
    },

    async sendChatMessage(message: Omit<AIChatMessage, 'id' | 'timestamp'>): Promise<AIChatMessage | null> {
      this.isLoading = true
      this.error = null
      const startTime = Date.now()
      try {
        const response = await axios.post<AIChatMessage>(
          '/api/ai/chat/',
          message
        )
        const chatResponse: AIChatMessage = {
          ...response.data,
          timestamp: response.data.timestamp || new Date().toISOString()
        }
        this.chatHistory.push(chatResponse)
        this.responses.push({
          type: 'chat',
          content: chatResponse,
          timestamp: new Date(),
          tokensUsed: (chatResponse?.message?.length || 0) +
            (chatResponse?.context?.length || 0)
        })
        this.updateUsage(
          (chatResponse?.message?.length || 0) +
          (chatResponse?.context?.length || 0),
          Date.now() - startTime
        )
        return chatResponse
      } catch (error: any) {
        this.error = error?.response?.data?.message || 'Falha ao enviar mensagem'
        console.error('Erro no chat AI:', error)
        return null
      } finally {
        this.isLoading = false
      }
    },

    async generateExam(request: AIGenerateExamRequest): Promise<AIExamSuggestion | null> {
      this.isLoading = true
      this.error = null
      const startTime = Date.now()
      try {
        const response = await axios.post<AIExamSuggestion>(
          '/api/ai/generate-exam/',
          request
        )
        const exam: AIExamSuggestion = {
          ...response.data,
          generatedAt: response.data.generatedAt || new Date().toISOString()
        }
        this.responses.push({
          type: 'exam',
          content: exam,
          timestamp: new Date(),
          tokensUsed: JSON.stringify(exam).length
        })
        this.updateUsage(
          JSON.stringify(exam).length,
          Date.now() - startTime
        )
        return exam
      } catch (error: any) {
        this.error = error?.response?.data?.message || 'Falha ao gerar prova'
        console.error('Erro ao gerar prova:', error)
        return null
      } finally {
        this.isLoading = false
      }
    },

    updateUsage(contentLength: number, responseTime: number): void {
      const estimatedTokens = Math.ceil(contentLength / 4)
      this.usage.tokens += estimatedTokens
      this.usage.requests += 1
      this.usage.lastRequest = new Date()
      const prevAvg = this.usage.averageResponseTime || 0
      const prevCount = this.usage.requests - 1
      this.usage.averageResponseTime =
        prevCount > 0
          ? (prevAvg * prevCount + responseTime) / this.usage.requests
          : responseTime
      const costPerToken = 0.000045
      this.usage.totalCost = (this.usage.totalCost || 0) + (estimatedTokens * costPerToken)
    },

    clearHistory(): void {
      this.responses = []
      this.generatedActivities = []
      this.generatedNotes = []
      this.chatHistory = []
      this.error = null
    },

    clearChat(): void {
      this.chatHistory = []
    },

    clearError(): void {
      this.error = null
    },

    resetUsage(): void {
      this.usage = {
        tokens: 0,
        requests: 0,
        lastRequest: undefined,
        averageResponseTime: 0,
        totalCost: 0
      }
    },

    removeActivity(activityId: string): void {
      this.generatedActivities = this.generatedActivities.filter(
        a => a.id !== activityId
      )
    },

    removeNote(index: number): void {
      if (index >= 0 && index < this.generatedNotes.length) {
        this.generatedNotes.splice(index, 1)
      }
    }
  },

  persist: {
    paths: ['usage', 'generatedActivities', 'generatedNotes', 'chatHistory']
  }
});