import { createPinia } from 'pinia'

const pinia = createPinia()

// Plugin customizado para persistência (sem dependências externas)
pinia.use(({ store }) => {
  // Lista de stores que queremos persistir
  const persistStores = ['auth', 'classroom', 'ai', 'dots']
  
  if (persistStores.includes(store.$id)) {
    // Carrega dados do sessionStorage ao inicializar
    const savedState = sessionStorage.getItem(`store-${store.$id}`)
    if (savedState) {
      try {
        const parsed = JSON.parse(savedState)
        store.$patch(parsed)
      } catch (e) {
        console.warn(`Erro ao carregar estado de ${store.$id}:`, e)
      }
    }

    // Salva automaticamente quando o estado mudar
    store.$subscribe((mutation, state) => {
      try {
        // Define quais campos salvar por store
        const persistPaths: Record<string, string[]> = {
          auth: ['token', 'refreshToken', 'user', 'isAuthenticated'],
          classroom: ['activeClassroom', 'lastUpdated'],
          ai: ['usage', 'generatedActivities', 'generatedNotes'],
          dots: ['profile']
        }

        const paths = persistPaths[store.$id] || []
        const stateToPersist: any = {}

        // Salva apenas os campos especificados
        paths.forEach(path => {
          if (path in state) {
            stateToPersist[path] = (state as any)[path]
          }
        })

        sessionStorage.setItem(`store-${store.$id}`, JSON.stringify(stateToPersist))
      } catch (e) {
        console.warn(`Erro ao salvar estado de ${store.$id}:`, e)
      }
    })
  }
})

// Re-exporta as stores
export { useAuthStore } from './auth'
export { useClassroomStore } from './classroom'
export { useAIStore } from './ai'
export { useDotsStore } from './dots'

export default pinia