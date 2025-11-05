<template>
  <div class="login">
    <div class="card">
      <h1 class="title">Entrar como Admin</h1>
      <p class="subtitle">Configurações, usuários e permissões</p>

      <form class="form" @submit.prevent="onSubmit">
        <input v-model="email" type="email" placeholder="E-mail do administrador" required />
        <input v-model="password" type="password" placeholder="Senha" required />
        <button type="submit" class="btn">Entrar</button>
      </form>

      <router-link to="/entrar/gestao" class="back">Trocar para outro acesso</router-link>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const email = ref('')
const password = ref('')

const onSubmit = () => {
  router.push({ name: 'admin-system-config' })
}
</script>

<style scoped>
.login { min-height: 100vh; display: grid; place-items: center; background: #fcfcfc; padding: 2rem; }
.card { width: 100%; max-width: 420px; background: #fcfcfc; border: 1.5px solid rgba(23,24,30,0.08); border-radius: 16px; padding: 2rem; text-align: center; }
.title { font-size: 1.6rem; font-weight: 800; color: #17181e; }
.subtitle { color: #6b6b6b; margin: 0.25rem 0 1.25rem; }
.form { display: grid; gap: 0.75rem; }
input { padding: 0.85rem 1rem; border: 1.5px solid rgba(23,24,30,0.12); border-radius: 10px; font-size: 0.95rem; background: #fff; }
.btn { padding: 0.9rem 1.2rem; background: #17181e; color: #fcfcfc; border: none; border-radius: 10px; font-weight: 700; cursor: pointer; }
.btn:hover { transform: translateY(-1px); box-shadow: 0 6px 16px rgba(23,24,30,0.2); }
.back { display: inline-block; margin-top: 1rem; color: #17181e; text-decoration: none; font-weight: 600; }
.back:hover { text-decoration: underline; }
</style>


