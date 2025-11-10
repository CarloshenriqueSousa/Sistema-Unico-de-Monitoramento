import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'

const app = createApp(App)

// APENAS UMA INSTÂNCIA!
const pinia = createPinia()
app.use(pinia)

app.use(router)

// ; antes da função
;(function() {
  const savedTheme = localStorage.getItem('theme') || 'light'
  if (savedTheme === 'dark') {
    document.documentElement.classList.add('dark')
  }
})()

// Global error handler
app.config.errorHandler = (err, instance, info) => {
  // Log não intrusivo e caminho para observabilidade futura
  console.error('[Vue Error]', { err, info })
}

window.addEventListener('unhandledrejection', (e) => {
  console.error('[Promise Rejection]', e.reason)
})

app.mount('#app')