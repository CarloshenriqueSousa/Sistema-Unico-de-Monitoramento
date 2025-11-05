import { defineStore } from 'pinia'
import axios from 'axios'
import type { DotsProfile, Achievement } from '@/types/dots'

export interface DotsState {
  profile: DotsProfile | null
  leaderboard: any[]
  isLoading: boolean
  error: string | null
}

export const useDotsStore = defineStore('dots', {
  state: (): DotsState => ({
    profile: null,
    leaderboard: [],
    isLoading: false,
    error: null
  }),

  getters: {
    overallProgress: (state): number => {
      if (!state.profile || !state.profile.skills?.length) return 0
      const total = state.profile.skills.reduce((sum, skill) => sum + (skill.level || 0), 0)
      return Math.min(100, Math.floor((total / (state.profile.skills.length * 10)) * 100))
    },

    topSkills: (state): DotsProfile['skills'] => {
      if (!state.profile?.skills) return []
      return [...state.profile.skills]
        .sort((a, b) => (b.level || 0) - (a.level || 0))
        .slice(0, 3)
    },

    weakestSkills: (state): DotsProfile['skills'] => {
      if (!state.profile?.skills) return []
      return [...state.profile.skills]
        .sort((a, b) => (a.level || 0) - (b.level || 0))
        .slice(0, 3)
    },

    totalAchievements: (state): number => {
      if (!state.profile?.achievements) return 0
      return (
        (state.profile.achievements.academic?.length || 0) +
        (state.profile.achievements.sports?.length || 0) +
        (state.profile.achievements.arts?.length || 0) +
        (state.profile.achievements.community?.length || 0) +
        (state.profile.achievements.social?.length || 0) +
        (state.profile.achievements.technical?.length || 0)
      )
    },

    studentRank: (state): number => {
      if (!state.profile) return 0
      const index = state.leaderboard.findIndex(
        (student: any) => student.id === state.profile?.studentId || student.studentId === state.profile?.studentId
      )
      return index !== -1 ? index + 1 : 0
    }
  },

  actions: {
    async loadProfile(userId: number): Promise<boolean> {
      this.isLoading = true
      this.error = null
      try {
        const response = await axios.get(`/api/dots/profile/${userId}/`)
        this.profile = response.data
        return true
      } catch (error: any) {
        this.error = error?.response?.data?.message || 'Falha ao carregar perfil DOTS'
        console.error('Erro ao carregar perfil DOTS:', error)
        return false
      } finally {
        this.isLoading = false
      }
    },

    async loadLeaderboard(classroomId?: number): Promise<boolean> {
      this.isLoading = true
      this.error = null
      try {
        const url = classroomId
          ? `/api/dots/leaderboard/?classroom=${classroomId}`
          : '/api/dots/leaderboard/'
        const response = await axios.get(url)
        this.leaderboard = response.data
        return true
      } catch (error: any) {
        this.error = error?.response?.data?.message || 'Falha ao carregar leaderboard'
        console.error('Erro ao carregar leaderboard:', error)
        return false
      } finally {
        this.isLoading = false
      }
    },

    async addAchievement(achievement: Omit<Achievement, 'id' | 'awardedAt'>): Promise<boolean> {
      if (!this.profile) return false

      this.isLoading = true
      this.error = null

      try {
        const response = await axios.post('/api/dots/achievements/', {
          ...achievement,
          studentId: this.profile.studentId
        })

        const newAchievement = response.data

        // Determina a categoria baseada nas propriedades do achievement
        if ('subject' in achievement && this.profile.achievements.academic) {
          this.profile.achievements.academic.push(newAchievement)
        } else if ('sport' in achievement && this.profile.achievements.sports) {
          this.profile.achievements.sports.push(newAchievement)
        } else if ('type' in achievement && this.profile.achievements.arts) {
          this.profile.achievements.arts.push(newAchievement)
        } else if ('organization' in achievement && this.profile.achievements.community) {
          this.profile.achievements.community.push(newAchievement)
        } else if ('category' in achievement) {
          // Social achievement
          if (!this.profile.achievements.social) {
            this.profile.achievements.social = []
          }
          this.profile.achievements.social.push(newAchievement)
        } else if ('technology' in achievement) {
          // Technical achievement
          if (!this.profile.achievements.technical) {
            this.profile.achievements.technical = []
          }
          this.profile.achievements.technical.push(newAchievement)
        }

        return true
      } catch (error: any) {
        this.error = error?.response?.data?.message || 'Falha ao adicionar conquista'
        console.error('Erro ao adicionar conquista:', error)
        return false
      } finally {
        this.isLoading = false
      }
    },

    async updateSkill(skillName: string, value: number): Promise<boolean> {
      if (!this.profile) return false

      this.error = null

      try {
        await axios.patch(`/api/dots/skills/${this.profile.studentId}/`, {
          skill: skillName,
          value
        })

        const skill = this.profile.skills.find(s => s.name === skillName)
        if (skill) {
          skill.level = Math.max(0, Math.min(10, value)) // Clamp entre 0 e 10
        }

        return true
      } catch (error: any) {
        this.error = error?.response?.data?.message || 'Erro ao atualizar habilidade'
        console.error('Erro ao atualizar habilidade:', error)
        return false
      }
    },

    async updateMultipleSkills(skills: Array<{ name: string; value: number }>): Promise<boolean> {
      if (!this.profile) return false

      this.isLoading = true
      this.error = null

      try {
        await axios.patch(`/api/dots/skills/${this.profile.studentId}/bulk/`, {
          skills
        })

        skills.forEach(({ name, value }) => {
          const skill = this.profile!.skills.find(s => s.name === name)
          if (skill) {
            skill.level = Math.max(0, Math.min(10, value))
          }
        })

        return true
      } catch (error: any) {
        this.error = error?.response?.data?.message || 'Erro ao atualizar habilidades'
        console.error('Erro ao atualizar habilidades:', error)
        return false
      } finally {
        this.isLoading = false
      }
    },

    async syncWithExternal(service: 'google' | 'microsoft'): Promise<boolean> {
      if (!this.profile) return false

      this.isLoading = true
      this.error = null

      try {
        const response = await axios.post(`/api/dots/sync/${service}/`, {
          studentId: this.profile.studentId
        })

        if (this.profile) {
          Object.assign(this.profile, response.data)
        }

        return true
      } catch (error: any) {
        this.error = error?.response?.data?.message || `Falha na sincronização com ${service}`
        console.error(`Erro na sincronização com ${service}:`, error)
        return false
      } finally {
        this.isLoading = false
      }
    },

    async refreshProfile(): Promise<boolean> {
      if (!this.profile) return false
      return await this.loadProfile(this.profile.studentId)
    },

    clearError(): void {
      this.error = null
    },

    resetProfile(): void {
      this.profile = null
      this.leaderboard = []
      this.error = null
    }
  }

  // REMOVIDO: persist - será tratado pelo plugin em store/index.ts
})