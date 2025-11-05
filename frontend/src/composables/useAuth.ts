import { ref, computed, onUnmounted } from 'vue'
import { useAuthStore } from '@/store/auth'
import { useRouter } from 'vue-router'

interface LoginCredentials {
  email: string
  password: string
}

interface TokenPayload {
  exp: number
  user_id: number
  email: string
  role?: string
}

export const useAuth = () => {
  const store = useAuthStore()
  const router = useRouter()
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  // Computed properties
  const isAuthenticated = computed(() => store.isAuthenticated)
  const user = computed(() => store.user)
  const userRole = computed(() => store.userRole)
  const userName = computed(() => store.userName)

  // Login
  const login = async (credentials: LoginCredentials): Promise<boolean> => {
    isLoading.value = true
    error.value = null
    
    try {
      await store.login(credentials)
      router.push({ name: 'Dashboard' })
      return true
    } catch (err: any) {
      error.value = err.response?.data?.message || 'Credenciais inválidas'
      console.error('Erro no login:', err)
      return false
    } finally {
      isLoading.value = false
    }
  }

  // Logout
  const logout = (): void => {
    store.logout()
    router.push({ name: 'Login' })
  }

  // Refresh token
  const refreshToken = async (): Promise<boolean> => {
    try {
      const success = await store.refreshAccessToken()
      if (!success) {
        logout()
      }
      return success
    } catch (err) {
      console.error('Erro ao renovar token:', err)
      logout()
      return false
    }
  }

  // Check if user has specific permission/role
  const hasPermission = (requiredRole: string): boolean => {
    if (!store.user) return false
    
    const currentRole = store.user.role?.toLowerCase()
    const required = requiredRole.toLowerCase()
    
    // Admin tem acesso a tudo
    if (currentRole === 'admin') return true
    
    // Comparação direta
    return currentRole === required
  }

  // Check multiple permissions (OR logic)
  const hasAnyPermission = (roles: string[]): boolean => {
    return roles.some(role => hasPermission(role))
  }

  // Check multiple permissions (AND logic)
  const hasAllPermissions = (roles: string[]): boolean => {
    return roles.every(role => hasPermission(role))
  }

  // Decode JWT token (sem dependência externa)
  const getTokenData = (): TokenPayload | null => {
    if (!store.token) return null
    
    try {
      const base64Url = store.token.split('.')[1]
      if (!base64Url) return null
      
      const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/')
      const jsonPayload = decodeURIComponent(
        atob(base64)
          .split('')
          .map(c => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
          .join('')
      )
      
      return JSON.parse(jsonPayload) as TokenPayload
    } catch (err) {
      console.error('Erro ao decodificar token:', err)
      return null
    }
  }

  // Check if token is expired
  const isTokenExpired = (): boolean => {
    const tokenData = getTokenData()
    if (!tokenData || !tokenData.exp) return true
    
    const expirationTime = tokenData.exp * 1000
    const currentTime = Date.now()
    
    return currentTime >= expirationTime
  }

  // Check if token will expire soon (default: 5 minutes)
  const isTokenExpiringSoon = (bufferMinutes: number = 5): boolean => {
    const tokenData = getTokenData()
    if (!tokenData || !tokenData.exp) return true
    
    const expirationTime = tokenData.exp * 1000
    const currentTime = Date.now()
    const bufferTime = bufferMinutes * 60 * 1000
    
    return currentTime >= (expirationTime - bufferTime)
  }

  // Auto refresh token setup
  let refreshInterval: number | null = null

  const setupAutoRefresh = (checkIntervalMinutes: number = 5): void => {
    // Limpa intervalo existente
    if (refreshInterval) {
      clearInterval(refreshInterval)
    }

    // Verifica token a cada X minutos
    refreshInterval = window.setInterval(() => {
      if (store.token && isTokenExpiringSoon()) {
        console.log('Token expirando em breve, renovando...')
        refreshToken()
      }
    }, checkIntervalMinutes * 60 * 1000)
  }

  const stopAutoRefresh = (): void => {
    if (refreshInterval) {
      clearInterval(refreshInterval)
      refreshInterval = null
    }
  }

  // Clear error
  const clearError = (): void => {
    error.value = null
    store.clearError()
  }

  // Update user data
  const updateUser = (userData: Partial<typeof store.user>): void => {
    if (userData) {
      store.updateUser(userData)
    }
  }

  // Setup auto refresh on mount
  setupAutoRefresh()

  // Cleanup on unmount
  onUnmounted(() => {
    stopAutoRefresh()
  })

  return {
    // State
    isLoading,
    error,
    
    // Computed
    isAuthenticated,
    user,
    userRole,
    userName,
    
    // Actions
    login,
    logout,
    refreshToken,
    hasPermission,
    hasAnyPermission,
    hasAllPermissions,
    getTokenData,
    isTokenExpired,
    isTokenExpiringSoon,
    setupAutoRefresh,
    stopAutoRefresh,
    clearError,
    updateUser
  }
}