import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { User } from '@/types/user'
import api from '@/services/api'

interface LoginCredentials {
  email: string
  password: string
}

interface TokenResponse {
  access: string
  refresh: string
}

export const useAuthStore = defineStore('auth', () => {
  // State
  const user = ref<User | null>(null)
  const token = ref<string | null>(null)
  const refreshToken = ref<string | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  // Computed
  const isAuthenticated = computed(() => !!token.value && !!user.value)
  const userRole = computed(() => user.value?.role || null)
  const userName = computed(() => user.value?.name || '')

  // Actions
  const login = async (credentials: LoginCredentials): Promise<void> => {
    loading.value = true
    error.value = null
    
    try {
      const response = await api.post<TokenResponse>('/api/token/', credentials)
      
      token.value = response.data.access
      refreshToken.value = response.data.refresh
      
      // Busca dados do usuário
      const userResponse = await api.get<User>('/api/user/me/', {
        headers: {
          Authorization: `Bearer ${token.value}`
        }
      })
      
      user.value = userResponse.data
      
      // Persiste no localStorage
      localStorage.setItem('token', token.value)
      localStorage.setItem('refreshToken', refreshToken.value)
      localStorage.setItem('user', JSON.stringify(user.value))
      
    } catch (err: any) {
      error.value = err.response?.data?.message || 'Credenciais inválidas'
      console.error('Erro no login:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const logout = (): void => {
    user.value = null
    token.value = null
    refreshToken.value = null
    error.value = null
    
    localStorage.removeItem('token')
    localStorage.removeItem('refreshToken')
    localStorage.removeItem('user')
  }

  const refreshAccessToken = async (): Promise<boolean> => {
    if (!refreshToken.value) {
      logout()
      return false
    }

    try {
      const response = await api.post<{ access: string }>('/api/token/refresh/', {
        refresh: refreshToken.value
      })
      
      token.value = response.data.access
      localStorage.setItem('token', token.value)
      
      return true
    } catch (err: any) {
      console.error('Erro ao renovar token:', err)
      logout()
      return false
    }
  }

  const checkAuth = (): void => {
    const tokenVal = localStorage.getItem('token')
    const refreshVal = localStorage.getItem('refreshToken')
    const userData = localStorage.getItem('user')
    
    if (tokenVal && userData) {
      try {
        user.value = JSON.parse(userData)
        token.value = tokenVal
        refreshToken.value = refreshVal
      } catch (err) {
        console.error('Erro ao recuperar dados do localStorage:', err)
        logout()
      }
    } else {
      logout()
    }
  }

  const updateUser = (userData: Partial<User>): void => {
    if (user.value) {
      user.value = { ...user.value, ...userData }
      localStorage.setItem('user', JSON.stringify(user.value))
    }
  }

  const clearError = (): void => {
    error.value = null
  }

  // Inicializa verificando auth
  checkAuth()

  return {
    // State
    user,
    token,
    refreshToken,
    loading,
    error,
    
    // Computed
    isAuthenticated,
    userRole,
    userName,
    
    // Actions
    login,
    logout,
    refreshAccessToken,
    checkAuth,
    updateUser,
    clearError
  }
})