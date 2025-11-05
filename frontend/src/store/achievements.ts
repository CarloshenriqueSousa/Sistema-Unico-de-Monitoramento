import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Achievement } from '@/types/achievements'

export const useAchievementsStore = defineStore('achievements', () => {
  const achievements = ref<Achievement[]>([])
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  async function fetchAchievements() {
    try {
      isLoading.value = true
      error.value = null

      // Mock temporário
      await new Promise(resolve => setTimeout(resolve, 500))
      achievements.value = [
        {
          id: 'a1',
          title: 'Primeiro Projeto Concluído',
          description: 'Você finalizou seu primeiro projeto!',
          points: 150,
          date: '2025-10-01',
          icon: '🏆',
          badges: [
            { id: 'b1', name: 'Iniciante', color: '#FFD700', icon: '⭐' }
          ]
        }
      ]
    } catch (err: any) {
      error.value = err.message || 'Erro ao carregar conquistas.'
    } finally {
      isLoading.value = false
    }
  }

  return { achievements, isLoading, error, fetchAchievements }
})
