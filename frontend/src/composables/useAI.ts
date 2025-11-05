import { ref, computed } from 'vue'
import OpenAI from 'openai'
import { useAuth } from './useAuth'
import { useAIStore } from '@/store/ai'
import type {
  AIGenerateActivityRequest,
  AIGenerateNotesRequest,
  AIGenerateExamRequest,
  AIStreamOptions,
  AICacheEntry
} from '@/types/ai'

// ============================================
// COMPOSABLE DEFINITION
// ============================================

export const useAI = () => {
  const { user } = useAuth()
  const store = useAIStore()
  
  // State local
  const isLoading = ref(false)
  const error = ref<string | null>(null)
  const streamContent = ref('')
  
  // Cache em memória com Map (melhor performance)
  const aiCache = ref<Map<string, AICacheEntry>>(new Map())
  
  // Configurações
  const CACHE_TTL = 60 * 60 * 1000 // 1 hora
  const DEFAULT_MODEL = 'gpt-4-turbo'
  const MAX_CACHE_SIZE = 100 // Limite de entradas no cache

  // ============================================
  // COMPUTED PROPERTIES
  // ============================================

  const generatedActivities = computed(() => store.generatedActivities)
  const generatedNotes = computed(() => store.generatedNotes)
  const chatHistory = computed(() => store.chatHistory)
  const usage = computed(() => store.usage)
  const hasError = computed(() => store.hasError)

  // ============================================
  // CACHE MANAGEMENT
  // ============================================

  /**
   * Limpar cache expirado
   */
  const clearExpiredCache = (): void => {
    const now = Date.now()
    const entries = Array.from(aiCache.value.entries())
    
    entries.forEach(([key, value]) => {
      if (now >= value.expiresAt) {
        aiCache.value.delete(key)
      }
    })
  }

  /**
   * Limpar cache se exceder limite
   */
  const limitCacheSize = (): void => {
    if (aiCache.value.size > MAX_CACHE_SIZE) {
      // Remove as 20 entradas mais antigas
      const entries = Array.from(aiCache.value.entries())
        .sort((a, b) => a[1].timestamp - b[1].timestamp)
      
      entries.slice(0, 20).forEach(([key]) => {
        aiCache.value.delete(key)
      })
    }
  }

  /**
   * Obter do cache
   */
  const getFromCache = (key: string): string | null => {
    clearExpiredCache()
    const cached = aiCache.value.get(key)
    
    if (cached && Date.now() < cached.expiresAt) {
      console.log('✅ Resposta obtida do cache')
      return cached.content
    }
    
    if (cached) {
      aiCache.value.delete(key) // Remove se expirado
    }
    
    return null
  }

  /**
   * Salvar no cache
   */
  const saveToCache = (key: string, content: string, model: string): void => {
    const now = Date.now()
    
    aiCache.value.set(key, {
      content,
      timestamp: now,
      expiresAt: now + CACHE_TTL,
      model
    })
    
    limitCacheSize()
  }

  /**
   * Limpar todo o cache
   */
  const clearCache = (): void => {
    aiCache.value.clear()
    console.log('🗑️ Cache limpo')
  }

  // ============================================
  // OPENAI CLIENT
  // ============================================

  /**
   * Obter cliente OpenAI configurado
   */
  const getClient = (): OpenAI => {
    const apiKey = import.meta.env.VITE_OPENAI_API_KEY
    
    if (!apiKey) {
      throw new Error('❌ OpenAI API Key não configurada. Verifique VITE_OPENAI_API_KEY no .env')
    }

    return new OpenAI({
      apiKey,
      dangerouslyAllowBrowser: true
    })
  }

  // ============================================
  // CORE AI FUNCTIONS
  // ============================================

  /**
   * Fazer pergunta à IA
   */
  const ask = async (
    query: string, 
    model: string = DEFAULT_MODEL,
    useCache: boolean = true
  ): Promise<string | null> => {
    if (!query || query.trim().length === 0) {
      error.value = 'Query não pode estar vazia'
      return null
    }

    const cacheKey = `${model}-${query}`
    
    // Verificar cache
    if (useCache) {
      const cached = getFromCache(cacheKey)
      if (cached) return cached
    }

    isLoading.value = true
    error.value = null
    streamContent.value = ''

    try {
      const client = getClient()
      const completion = await client.chat.completions.create({
        model,
        messages: [
          {
            role: 'system',
            content: `Você é um assistente educacional especializado no sistema S.U.M. (Sistema Unificado de Monitoria).

Contexto do usuário:
- Nome: ${user.value?.name || 'Usuário'}
- Role: ${user.value?.role || 'não especificado'}

Suas responsabilidades:
- Fornecer respostas precisas e educacionais
- Adaptar conteúdo ao contexto escolar brasileiro
- Ser claro, objetivo e profissional
- Quando solicitar JSON, retornar APENAS JSON válido, sem markdown`
          },
          {
            role: 'user',
            content: query
          }
        ],
        max_tokens: 1500,
        temperature: 0.7,
        top_p: 1,
        frequency_penalty: 0,
        presence_penalty: 0
      })
      
      const result = completion.choices[0]?.message?.content || ''
      
      if (!result) {
        throw new Error('Resposta vazia da OpenAI')
      }
      
      // Salvar no cache
      if (useCache) {
        saveToCache(cacheKey, result, model)
      }
      
      console.log(`✅ Resposta gerada (${result.length} caracteres)`)
      return result
      
    } catch (err: any) {
      const errorMessage = err.message || 'Erro desconhecido na IA'
      error.value = `Erro na IA: ${errorMessage}`
      console.error('❌ Erro ao consultar IA:', err)
      return null
    } finally {
      isLoading.value = false
    }
  }

  /**
   * Fazer pergunta com streaming
   */
  const streamAsk = async (
    query: string, 
    options?: AIStreamOptions,
    model: string = DEFAULT_MODEL
  ): Promise<string | null> => {
    if (!query || query.trim().length === 0) {
      error.value = 'Query não pode estar vazia'
      return null
    }

    isLoading.value = true
    error.value = null
    streamContent.value = ''

    try {
      const client = getClient()
      const stream = await client.chat.completions.create({
        model,
        messages: [
          {
            role: 'system',
            content: `Você é um assistente educacional do sistema S.U.M.
Usuário: ${user.value?.name || 'Usuário'} (${user.value?.role || 'não especificado'})`
          },
          {
            role: 'user',
            content: query
          }
        ],
        stream: true,
        max_tokens: 2000,
        temperature: 0.7
      })

      for await (const chunk of stream) {
        const content = chunk.choices[0]?.delta?.content || ''
        streamContent.value += content
        
        // Callback em tempo real
        if (options?.onChunk) {
          options.onChunk(streamContent.value)
        }
      }
      
      // Callback ao completar
      if (options?.onComplete) {
        options.onComplete(streamContent.value)
      }
      
      console.log(`✅ Stream completo (${streamContent.value.length} caracteres)`)
      return streamContent.value
      
    } catch (err: any) {
      const errorMessage = err.message || 'Erro desconhecido'
      error.value = `Erro no streaming: ${errorMessage}`
      console.error('❌ Erro no streaming:', err)
      
      if (options?.onError) {
        options.onError(err)
      }
      
      return null
    } finally {
      isLoading.value = false
    }
  }

  // ============================================
  // SPECIALIZED GENERATION FUNCTIONS
  // ============================================

  /**
   * Gerar atividade educacional
   */
  const generateActivity = async (
    request: AIGenerateActivityRequest
  ): Promise<string | null> => {
    const prompt = `Crie uma atividade educacional completa sobre "${request.topic}" para alunos de nível ${request.level}.

ESPECIFICAÇÕES:
- Assunto: ${request.subject || 'Não especificado'}
- Dificuldade: ${request.difficulty || 'medium'}
- Duração: ${request.duration || 45} minutos
- Tipo: ${request.type || 'individual'}

ESTRUTURA OBRIGATÓRIA:
1. Título criativo e relevante
2. Objetivos de aprendizagem (3-5 objetivos SMART)
3. Descrição detalhada da atividade
4. Materiais necessários
5. Passo a passo da execução
6. Critérios de avaliação claros
7. ${request.questionCount || 3} questões com alternativas múltiplas (A, B, C, D)
8. Gabarito com explicações

FORMATO: Retorne APENAS um JSON válido (sem markdown, sem \`\`\`json):
{
  "title": "Título da atividade",
  "objectives": ["objetivo1", "objetivo2", "objetivo3"],
  "description": "Descrição completa",
  "materials": ["material1", "material2"],
  "steps": ["passo1", "passo2"],
  "criteria": ["critério1", "critério2"],
  "questions": [
    {
      "question": "Pergunta?",
      "options": ["A) ...", "B) ...", "C) ...", "D) ..."],
      "correctAnswer": "A",
      "explanation": "Por que esta é a resposta correta"
    }
  ],
  "estimatedTime": ${request.duration || 45}
}`

    return await ask(prompt, DEFAULT_MODEL, false)
  }

  /**
   * Gerar anotações de estudo
   */
  const generateNotes = async (
    request: AIGenerateNotesRequest
  ): Promise<string | null> => {
    const format = request.format || 'detailed'
    
    const prompt = `Crie anotações de estudo sobre "${request.topic}" para um aluno com nível ${request.studentLevel}.

ESPECIFICAÇÕES:
- Assunto: ${request.subject || 'Não especificado'}
- Formato: ${format}
- Incluir exemplos: ${request.includeExamples !== false ? 'Sim' : 'Não'}
${request.focusAreas ? `- Focar em: ${request.focusAreas.join(', ')}` : ''}

ESTRUTURA:
1. 📚 Introdução clara ao tema
2. 🎯 Conceitos principais (3-5 conceitos-chave)
3. 💡 Exemplos práticos do cotidiano
4. 📝 Dicas de estudo e memorização
5. ✅ Resumo em tópicos
6. ❓ Questões para autoavaliação

Use emojis, linguagem acessível e formatação em Markdown.`

    return await ask(prompt, DEFAULT_MODEL, false)
  }

  /**
   * Gerar prova/exame
   */
  const generateExam = async (
    request: AIGenerateExamRequest
  ): Promise<string | null> => {
    const questionTypes = request.questionTypes || {
      multipleChoice: Math.ceil(request.questionCount * 0.6),
      essay: Math.ceil(request.questionCount * 0.3),
      trueFalse: Math.floor(request.questionCount * 0.1)
    }

    const prompt = `Crie uma prova completa com as seguintes especificações:

INFORMAÇÕES:
- Disciplina: ${request.subject}
- Tópicos: ${request.topics.join(', ')}
- Dificuldade: ${request.difficulty}
- Total de questões: ${request.questionCount}
- Duração: ${request.duration || 60} minutos

DISTRIBUIÇÃO:
- Múltipla escolha: ${questionTypes.multipleChoice} questões
- Dissertativas: ${questionTypes.essay} questões
- Verdadeiro/Falso: ${questionTypes.trueFalse} questões

FORMATO: Retorne APENAS JSON válido (sem markdown):
{
  "title": "Título da prova",
  "instructions": "Instruções claras aos alunos",
  "questions": [
    {
      "number": 1,
      "type": "multiple_choice|essay|true_false",
      "question": "Enunciado completo",
      "options": ["A) ...", "B) ...", "C) ...", "D) ..."],
      "correctAnswer": "resposta correta",
      "points": 10,
      "explanation": "Explicação didática"
    }
  ],
  "totalPoints": 100,
  "answerKey": "gabarito resumido"
}`

    return await ask(prompt, DEFAULT_MODEL, false)
  }

  /**
   * Analisar perfil DOTS
   */
  const analyzeDots = async (userId: number): Promise<string | null> => {
    try {
      const result = await store.analyzeDots(userId)
      return result ? JSON.stringify(result, null, 2) : null
    } catch (err) {
      error.value = 'Erro ao analisar perfil DOTS'
      console.error('❌ Erro DOTS:', err)
      return null
    }
  }

  /**
   * Otimizar sala de aula
   */
  const optimizeClassroom = async (classroomId: number): Promise<string | null> => {
    try {
      const result = await store.optimizeClassroom(classroomId)
      return result ? JSON.stringify(result, null, 2) : null
    } catch (err) {
      error.value = 'Erro ao otimizar sala de aula'
      console.error('❌ Erro otimização:', err)
      return null
    }
  }

  // ============================================
  // UTILITY FUNCTIONS
  // ============================================

  /**
   * Limpar erro
   */
  const clearError = (): void => {
    error.value = null
    store.clearError()
  }

  /**
   * Obter estatísticas do cache
   */
  const getCacheStats = () => ({
    size: aiCache.value.size,
    maxSize: MAX_CACHE_SIZE,
    ttl: CACHE_TTL,
    entries: Array.from(aiCache.value.entries()).map(([key, value]) => ({
      key,
      model: value.model,
      age: Date.now() - value.timestamp,
      expiresIn: value.expiresAt - Date.now()
    }))
  })

  // ============================================
  // RETURN
  // ============================================

  return {
    // State
    isLoading,
    error,
    streamContent,
    
    // Computed from store
    generatedActivities,
    generatedNotes,
    chatHistory,
    usage,
    hasError,
    
    // Core functions
    ask,
    streamAsk,
    
    // Specialized functions
    generateActivity,
    generateNotes,
    generateExam,
    analyzeDots,
    optimizeClassroom,
    
    // Utilities
    clearCache,
    clearError,
    getCacheStats
  }
}