import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { AchievementBadge } from '@/types/achievements'

export const useBadgesStore = defineStore('badges', () => {
  const badges = ref<AchievementBadge[]>([])
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  async function fetchBadges() {
    try {
      isLoading.value = true
      error.value = null

      // Mock temporário — trocar depois por chamada à API da escola
      await new Promise(resolve => setTimeout(resolve, 500))
      badges.value = [
        { id: 'b1', name: 'Líder de Turma', color: '#FFD700', icon: '👑' },
        { id: 'b2', name: 'Pontual', color: '#4CAF50', icon: '⏰' },
        { id: 'b3', name: 'Criativo', color: '#2196F3', icon: '🎨' },
        { id: 'b4', name: 'Colaborador', color: '#E91E63', icon: '🤝' }
      ]
    } catch (err: any) {
      error.value = err.message || 'Erro ao carregar badges.'
    } finally {
      isLoading.value = false
    }
  }

  function addBadge(badge: Omit<AchievementBadge, 'id'>) {
    badges.value.push({
      id: crypto.randomUUID(),
      ...badge
    })
  }

  function removeBadge(id: string) {
    badges.value = badges.value.filter(b => b.id !== id)
  }

  return { badges, isLoading, error, fetchBadges, addBadge, removeBadge }
})
