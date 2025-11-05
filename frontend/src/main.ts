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

app.mount('#app')