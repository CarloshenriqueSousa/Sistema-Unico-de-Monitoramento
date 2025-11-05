<template>
  <div class="layout-professor">
    <aside class="sidebar">
      <div class="logo">
        <span class="logo-icon">S</span>
        <span class="logo-text">S.U.M</span>
      </div>
      <nav class="nav">
        <router-link v-for="item in navItems" :key="item.path" :to="item.path" class="nav-link" :class="{ active: $route.path.startsWith(item.path) }">
          <i :class="item.icon"></i>
          <span>{{ item.name }}</span>
        </router-link>
      </nav>
      <button @click="logout" class="logout-btn">Sair</button>
    </aside>
    <main class="main">
      <router-view />
    </main>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/store/auth'

const router = useRouter()
const authStore = useAuthStore()

const navItems = [
  { name: 'Dashboard', path: '/professor/dashboard', icon: 'fas fa-th-large' },
  { name: 'Turmas', path: '/professor/class-management', icon: 'fas fa-chalkboard-teacher' },
  { name: 'IA Atividades', path: '/professor/ai-activities', icon: 'fas fa-robot' },
  { name: 'IA Notas', path: '/professor/ai-notes', icon: 'fas fa-file-invoice' },
  { name: 'Provas', path: '/professor/exams', icon: 'fas fa-clipboard-check' },
  { name: 'Análise', path: '/professor/student-analysis', icon: 'fas fa-chart-line' },
  { name: 'Chat', path: '/professor/chat', icon: 'fas fa-comments' }
]

function logout() {
  authStore.logout()
  router.push('/entrar')
}
</script>

<style scoped>
.layout-professor { display: flex; min-height: 100vh; background: #fcfcfc; }
.sidebar { width: 260px; background: #17181e; padding: 1.5rem; display: flex; flex-direction: column; }
.logo { display: flex; align-items: center; gap: 0.75rem; margin-bottom: 2rem; color: #fcfcfc; }
.logo-icon { width: 40px; height: 40px; background: linear-gradient(135deg, #10b981, #fbbf24); border-radius: 10px; display: flex; align-items: center; justify-content: center; font-weight: 800; }
.logo-text { font-size: 1.25rem; font-weight: 700; }
.nav { flex: 1; display: flex; flex-direction: column; gap: 0.5rem; }
.nav-link { display: flex; align-items: center; gap: 0.75rem; padding: 0.75rem 1rem; color: rgba(252,252,252,0.7); text-decoration: none; border-radius: 10px; transition: all 0.2s; }
.nav-link:hover { background: rgba(252,252,252,0.08); color: #fcfcfc; }
.nav-link.active { background: rgba(16,185,129,0.2); color: #10b981; }
.logout-btn { padding: 0.75rem 1rem; background: rgba(239,68,68,0.1); border: 1px solid rgba(239,68,68,0.2); border-radius: 10px; color: #ef4444; cursor: pointer; font-weight: 600; }
.logout-btn:hover { background: rgba(239,68,68,0.2); }
.main { flex: 1; padding: 2rem; overflow-y: auto; }
</style>

