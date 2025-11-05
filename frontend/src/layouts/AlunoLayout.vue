<template>
  <div class="layout-aluno">
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
  { name: 'Dashboard', path: '/aluno/dashboard', icon: 'fas fa-home' },
  { name: 'Sala de Aula', path: '/aluno/classroom', icon: 'fas fa-chalkboard' },
  { name: 'Atividades', path: '/aluno/activities', icon: 'fas fa-book' },
  { name: 'Avaliações', path: '/aluno/exams', icon: 'fas fa-file-alt' },
  { name: 'Anotações', path: '/aluno/notes', icon: 'fas fa-sticky-note' },
  { name: 'DOTS', path: '/aluno/dots', icon: 'fas fa-star' },
  { name: 'Chat', path: '/aluno/chat', icon: 'fas fa-comments' }
]

function logout() {
  authStore.logout()
  router.push('/entrar')
}
</script>

<style scoped>
.layout-aluno { display: flex; min-height: 100vh; background: #fcfcfc; }
.sidebar { width: 260px; background: #17181e; padding: 1.5rem; display: flex; flex-direction: column; }
.logo { display: flex; align-items: center; gap: 0.75rem; margin-bottom: 2rem; color: #fcfcfc; }
.logo-icon { width: 40px; height: 40px; background: linear-gradient(135deg, #2d531a, #0f1e3f); border-radius: 10px; display: flex; align-items: center; justify-content: center; font-weight: 800; }
.logo-text { font-size: 1.25rem; font-weight: 700; }
.nav { flex: 1; display: flex; flex-direction: column; gap: 0.5rem; }
.nav-link { display: flex; align-items: center; gap: 0.75rem; padding: 0.75rem 1rem; color: rgba(252,252,252,0.7); text-decoration: none; border-radius: 10px; transition: all 0.2s; }
.nav-link:hover { background: rgba(252,252,252,0.08); color: #fcfcfc; }
.nav-link.active { background: rgba(45,83,26,0.2); color: #2d531a; }
.logout-btn { padding: 0.75rem 1rem; background: rgba(239,68,68,0.1); border: 1px solid rgba(239,68,68,0.2); border-radius: 10px; color: #ef4444; cursor: pointer; font-weight: 600; }
.logout-btn:hover { background: rgba(239,68,68,0.2); }
.main { flex: 1; padding: 2rem; overflow-y: auto; }
</style>

