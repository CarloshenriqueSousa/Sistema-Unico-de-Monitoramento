import { ref, computed } from 'vue'
import { useDotsStore } from '@/store/dots'
import { useAI } from './useAI'
import type { Achievement } from '@/types/dots'

export const useDots = () => {
  const store = useDotsStore()
  const { ask } = useAI()
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  const profile = computed(() => store.profile)
  
  // CORRIGIDO: skills é um array de objetos { name, level, verified, category }
  const progress = computed(() => {
    if (!profile.value || !profile.value.skills || !Array.isArray(profile.value.skills)) {
      return 0
    }
    
    // Soma os níveis de todas as skills
    const totalPoints = profile.value.skills.reduce((sum, skill) => sum + skill.level, 0)
    const maxPoints = profile.value.skills.length * 10 // Cada skill vai de 0 a 10
    
    return maxPoints > 0 ? Math.min(100, Math.floor((totalPoints / maxPoints) * 100)) : 0
  })

  // Getter adicional: total de conquistas
  const totalAchievements = computed(() => {
    if (!profile.value?.achievements) return 0
    
    return (
      (profile.value.achievements.academic?.length || 0) +
      (profile.value.achievements.social?.length || 0) +
      (profile.value.achievements.technical?.length || 0)
    )
  })

  // Getter: skills mais fortes
  const topSkills = computed(() => {
    if (!profile.value?.skills) return []
    
    return [...profile.value.skills]
      .sort((a, b) => b.level - a.level)
      .slice(0, 3)
  })

  // Getter: skills mais fracas
  const weakSkills = computed(() => {
    if (!profile.value?.skills) return []
    
    return [...profile.value.skills]
      .sort((a, b) => a.level - b.level)
      .slice(0, 3)
  })

  const loadProfile = async (userId: number) => {
    isLoading.value = true
    error.value = null
    
    try {
      const success = await store.loadProfile(userId)
      if (!success) {
        error.value = store.error || 'Erro ao carregar perfil'
      }
      return success
    } catch (err: any) {
      error.value = err.message || 'Erro ao carregar perfil'
      return false
    } finally {
      isLoading.value = false
    }
  }

  const addAchievement = async (achievementData: {
    title: string
    description: string
    icon?: string
    category?: 'academic' | 'social' | 'technical'
  }) => {
    isLoading.value = true
    error.value = null
    
    try {
      const achievement: Omit<Achievement, 'id' | 'awardedAt'> = {
        title: achievementData.title,
        description: achievementData.description,
        icon: achievementData.icon || '🏆',
        category: achievementData.category
      }
      
      const success = await store.addAchievement(achievement)
      
      if (!success) {
        error.value = store.error || 'Erro ao adicionar conquista'
      }
      
      return success
    } catch (err: any) {
      error.value = err.message || 'Erro ao adicionar conquista'
      return false
    } finally {
      isLoading.value = false
    }
  }

  const updateSkill = async (skillName: string, newLevel: number) => {
    isLoading.value = true
    error.value = null
    
    try {
      const success = await store.updateSkill(skillName, newLevel)
      
      if (!success) {
        error.value = 'Erro ao atualizar habilidade'
      }
      
      return success
    } catch (err: any) {
      error.value = err.message || 'Erro ao atualizar habilidade'
      return false
    } finally {
      isLoading.value = false
    }
  }

  const analyzeProgress = async () => {
    if (!profile.value) {
      error.value = 'Perfil não carregado'
      return null
    }

    isLoading.value = true
    error.value = null
    
    try {
      const prompt = `Analise o perfil DOTS do aluno:

**Habilidades:**
${profile.value.skills.map(s => `- ${s.name}: ${s.level}/10`).join('\n')}

**Conquistas:**
- Acadêmicas: ${profile.value.achievements?.academic?.length || 0}
- Sociais: ${profile.value.achievements?.social?.length || 0}
- Técnicas: ${profile.value.achievements?.technical?.length || 0}

**Progresso geral:** ${progress.value}%

Forneça uma análise detalhada em markdown com:

## 💪 Pontos Fortes
(Liste 3 principais forças com base nas habilidades mais altas)

## 📈 Áreas de Desenvolvimento
(Liste 3 áreas com maior potencial de crescimento)

## 🎯 Sugestões de Atividades
(Sugira 4-5 atividades específicas para desenvolver as áreas identificadas)

## 📊 Projeção de Desenvolvimento
(Previsão de evolução nos próximos 3 meses se seguir as recomendações)`
      
      const response = await ask(prompt)
      return response
    } catch (err: any) {
      error.value = err.message || 'Erro na análise de progresso'
      return null
    } finally {
      isLoading.value = false
    }
  }

  const compareWithClass = async (classroomId?: number) => {
    if (!profile.value) {
      error.value = 'Perfil não carregado'
      return null
    }

    isLoading.value = true
    error.value = null
    
    try {
      // Carrega leaderboard para comparação
      if (classroomId) {
        await store.loadLeaderboard(classroomId)
      }

      const prompt = `Compare o perfil do aluno com a turma:

**Perfil do Aluno:**
${profile.value.skills.map(s => `- ${s.name}: ${s.level}/10`).join('\n')}
Progresso: ${progress.value}%
Total de conquistas: ${totalAchievements.value}

**Posição na turma:** ${store.studentRank > 0 ? `${store.studentRank}º lugar` : 'Não classificado'}

Com base nisso, forneça uma análise comparativa em markdown:

## 🌟 Áreas de Destaque
(2 áreas onde o aluno se sobressai em relação à média da turma)

## 📚 Área para Desenvolvimento Prioritário
(1 área específica que merece atenção especial)

## 💡 Recomendações Personalizadas
(Sugestões práticas considerando o desempenho relativo à turma)

## 🎓 Perspectiva do Professor
(Como orientar este aluno considerando seu perfil único)`
      
      const response = await ask(prompt)
      return response
    } catch (err: any) {
      error.value = err.message || 'Erro na comparação com a turma'
      return null
    } finally {
      isLoading.value = false
    }
  }

  const syncWithExternal = async (service: 'google' | 'microsoft') => {
    isLoading.value = true
    error.value = null
    
    try {
      const success = await store.syncWithExternal(service)
      
      if (!success) {
        error.value = store.error || `Erro ao sincronizar com ${service}`
      }
      
      return success
    } catch (err: any) {
      error.value = err.message || `Erro ao sincronizar com ${service}`
      return false
    } finally {
      isLoading.value = false
    }
  }

  const refreshProfile = async () => {
    isLoading.value = true
    error.value = null
    
    try {
      const success = await store.refreshProfile()
      
      if (!success) {
        error.value = 'Erro ao atualizar perfil'
      }
      
      return success
    } catch (err: any) {
      error.value = err.message || 'Erro ao atualizar perfil'
      return false
    } finally {
      isLoading.value = false
    }
  }

  const clearError = () => {
    error.value = null
    store.clearError()
  }

  return {
    // State
    profile,
    progress,
    totalAchievements,
    topSkills,
    weakSkills,
    isLoading,
    error,
    leaderboard: computed(() => store.leaderboard),
    studentRank: computed(() => store.studentRank),
    
    // Actions
    loadProfile,
    addAchievement,
    updateSkill,
    analyzeProgress,
    compareWithClass,
    syncWithExternal,
    refreshProfile,
    clearError,
  }
}