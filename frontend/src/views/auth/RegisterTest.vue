<template>
  <div class="register-root">
    <div class="card">
      <h2>Cadastro de Teste</h2>
      <p class="subtitle">Crie um usuário mock para testar acesso por perfil</p>
      <form @submit.prevent="submit">
        <div class="row">
          <label>Nome</label>
          <input v-model="name" type="text" required />
        </div>
        <div class="row">
          <label>Email</label>
          <input v-model="email" type="email" required />
        </div>
        <div class="row">
          <label>Senha</label>
          <input v-model="password" type="password" required />
        </div>
        <div class="row">
          <label>Perfil</label>
          <select v-model="role" required>
            <option value="Aluno">Aluno</option>
            <option value="Professor">Professor</option>
            <option value="Gestor">Escola (Gestor)</option>
            <option value="Admin">Admin</option>
          </select>
        </div>
        <button class="btn" type="submit">Criar e Entrar</button>
        <router-link class="link" to="/entrar">Voltar</router-link>
      </form>
    </div>
  </div>
  
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/store/auth'

const router = useRouter()
const auth = useAuthStore()

const name = ref('')
const email = ref('')
const password = ref('')
const role = ref<'Aluno'|'Professor'|'Gestor'|'Admin'>('Aluno')

function submit() {
  // Cria usuário e tokens no localStorage conforme o auth store espera
  const user = { id: 1, name: name.value, email: email.value, role: role.value }
  localStorage.setItem('user', JSON.stringify(user))
  localStorage.setItem('token', 'mock-token')
  localStorage.setItem('refreshToken', 'mock-refresh')
  auth.checkAuth()
  const routeByRole: Record<string, string> = {
    'Aluno': 'aluno-dashboard',
    'Professor': 'professor-dashboard',
    'Gestor': 'escola-dashboard',
    'Admin': 'admin-system-config'
  }
  router.push({ name: routeByRole[role.value] || 'showcase' })
}
</script>

<style scoped>
.register-root { display:flex; align-items:center; justify-content:center; min-height: 100vh; background:#f5f5f7; padding: 2rem; }
.card { width: 100%; max-width: 420px; background:#fff; border:1px solid rgba(23,24,30,0.08); border-radius:16px; padding:1.25rem 1.25rem 1rem; }
h2 { margin:0 0 0.25rem 0; color:#17181e; font-size:1.4rem; }
.subtitle { margin:0 0 1rem 0; color:#6b6b6b; font-size:0.9rem; }
form { display:flex; flex-direction:column; gap:0.75rem; }
.row { display:flex; flex-direction:column; gap:0.3rem; }
label { font-size:0.85rem; color:#374151; }
input, select { padding:0.55rem 0.7rem; border:1px solid rgba(23,24,30,0.12); border-radius:10px; font-size:0.95rem; }
.btn { margin-top:0.5rem; padding:0.65rem 0.9rem; background:#17181e; color:#fff; border:none; border-radius:10px; font-weight:600; cursor:pointer; }
.btn:hover { filter: brightness(0.95); }
.link { display:inline-block; margin-top:0.5rem; color:#374151; text-decoration:none; font-size:0.9rem; }
.link:hover { text-decoration:underline; }
</style>


