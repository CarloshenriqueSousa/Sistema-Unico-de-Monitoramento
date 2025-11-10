<template>
  <footer class="app-footer">
    <div class="container">
      <div class="left">
        <strong>S.U.M</strong>
        <span>© 2025 - Todos os direitos reservados</span>
      </div>
      <nav class="right">
        <router-link :to="{ name: 'showcase', hash: '#features' }">Funcionalidades</router-link>
        <router-link :to="{ name: 'showcase', hash: '#demos' }">Demos</router-link>
        <router-link :to="{ name: 'entrar' }">Entrar</router-link>
      </nav>
    </div>
  </footer>
</template>

<script setup lang="ts">
</script>

<style scoped>
.app-footer { background: #f8f9fa; border-top: 1px solid rgba(23,24,28,.08); margin-top: 2rem }
.container { max-width: 1200px; margin: 0 auto; padding: 1rem; display: flex; align-items: center; justify-content: space-between }
.left { display: flex; gap: .75rem; align-items: center; color: #6b7280 }
.right { display: flex; gap: 1rem }
.right a { color: #6b7280; text-decoration: none; font-weight: 600 }
.right a:hover { color: #17181c }
</style>


