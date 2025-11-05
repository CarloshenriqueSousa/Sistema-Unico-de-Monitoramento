// types/ai.ts

// ============================================
// TIPOS BASE
// ============================================

export type QuestionType = 'multiple_choice' | 'open' | 'true_false' | 'essay'
export type DifficultyLevel = 'easy' | 'medium' | 'hard'
export type RiskLevel = 'low' | 'medium' | 'high'
export type ActivityType = 'individual' | 'group' | 'pair'
export type OptimizationType = 'seating' | 'grouping' | 'activity'
export type PriorityLevel = 'low' | 'medium' | 'high'

// ============================================
// QUESTÕES E ATIVIDADES
// ============================================

export interface AIQuestion {
  id: string
  text: string
  type: QuestionType
  options?: string[]
  correctAnswer?: string | number
  explanation?: string
  points?: number
}

export interface AIActivitySuggestion {
  id: string
  title: string
  prompt: string
  content: string
  generatedAt: string
  generatedBy: string
  subject: string
  difficulty: DifficultyLevel
  tags?: string[]
  objectives?: string[]
  description?: string
  criteria?: string[]
  questions?: AIQuestion[]
  estimatedTime?: number
  type?: ActivityType
}

// ============================================
// PROVAS E AVALIAÇÕES
// ============================================

export interface AIExamSuggestion {
  id: string
  title: string
  instructions?: string
  questions: AIQuestion[]
  generatedAt: string
  generatedBy: string
  subject: string
  difficulty: DifficultyLevel
  totalPoints?: number
  duration?: number
  topics?: string[]
}

// ============================================
// CHAT E MENSAGENS
// ============================================

export interface AIChatMessage {
  id: string
  sender: 'user' | 'ai'
  message: string
  timestamp: string
  context?: string
  metadata?: Record<string, any>
}

// ============================================
// ANÁLISES E RELATÓRIOS
// ============================================

export interface AIAnalysisReport {
  id: string
  studentId: string | number
  generatedAt: string
  summary: string
  recommendations: string[]
  riskLevel: RiskLevel
  strengths?: string[]
  weaknesses?: string[]
  actionPlan?: string[]
  scores?: {
    academic?: number
    behavioral?: number
    social?: number
  }
}

// ============================================
// OTIMIZAÇÃO DE SALA DE AULA
// ============================================

export interface AIOptimizationSuggestion {
  type: OptimizationType
  description: string
  priority: PriorityLevel
  implementation?: string
  expectedOutcome?: string
  estimatedImpact?: number
}

export interface AIOptimizationResult {
  classroomId: number
  suggestions: AIOptimizationSuggestion[]
  reasoning: string
  expectedOutcomes: string[]
  generatedAt?: string
  appliedAt?: string
}

// ============================================
// REQUESTS (Requisições para IA)
// ============================================

export interface AIGenerateActivityRequest {
  topic: string
  level: string
  subject?: string
  duration?: number
  type?: ActivityType
  difficulty?: DifficultyLevel
  questionCount?: number
}

export interface AIGenerateNotesRequest {
  topic: string
  studentLevel: string
  subject?: string
  focusAreas?: string[]
  format?: 'outline' | 'detailed' | 'summary'
  includeExamples?: boolean
}

export interface AIGenerateExamRequest {
  subject: string
  topics: string[]
  difficulty: DifficultyLevel
  questionCount: number
  duration?: number
  questionTypes?: {
    multipleChoice?: number
    essay?: number
    trueFalse?: number
  }
}

export interface AIAnalyzeDotsRequest {
  userId: number
  includeHistory?: boolean
  timeFrame?: 'week' | 'month' | 'semester' | 'year'
}

export interface AIOptimizeClassroomRequest {
  classroomId: number
  objectives?: string[]
  constraints?: string[]
  preferredLayout?: 'rows' | 'groups' | 'circle' | 'horseshoe'
}

// ============================================
// ESTATÍSTICAS E USO
// ============================================

export interface AIUsageStats {
  tokens: number
  requests: number
  lastRequest?: Date
  averageResponseTime?: number
  totalCost?: number
}

export interface AIResponse {
  type: string
  content: any
  timestamp: Date
  tokensUsed?: number
  model?: string
}

// ============================================
// CONFIGURAÇÕES
// ============================================

export interface AIConfig {
  model: string
  temperature: number
  maxTokens: number
  topP?: number
  frequencyPenalty?: number
  presencePenalty?: number
}

export interface AICacheEntry {
  content: string
  timestamp: number
  expiresAt: number
  model: string
}

// ============================================
// TIPOS DE RETORNO DE FUNÇÕES
// ============================================

export interface AIGenerationResult<T = any> {
  success: boolean
  data?: T
  error?: string
  tokensUsed?: number
  timeElapsed?: number
}

export interface AIStreamOptions {
  onChunk?: (content: string) => void
  onComplete?: (content: string) => void
  onError?: (error: Error) => void
}