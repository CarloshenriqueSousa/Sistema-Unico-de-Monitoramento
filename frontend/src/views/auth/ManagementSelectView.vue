<template>
  <div class="auth-select">
    <div class="auth-card">
      <h1 class="title">Acesso de Gestão</h1>
      <p class="subtitle">Escolha como deseja administrar o sistema</p>

      <div class="options">
        <router-link to="/login/escola" class="option">
          <div class="icon">🏫</div>
          <div class="content">
            <h3>Escola</h3>
            <p>Gestão acadêmica, relatórios e organização</p>
          </div>
        </router-link>

        <router-link to="/login/admin" class="option">
          <div class="icon">🛡️</div>
          <div class="content">
            <h3>Administrador</h3>
            <p>Configurações do sistema, usuários e permissões</p>
          </div>
        </router-link>
      </div>

      <router-link to="/entrar" class="secondary-link">Voltar</router-link>
    </div>
  </div>
</template>

<script setup lang="ts"></script>

<style scoped>
.auth-select { min-height: 100vh; display: grid; place-items: center; background: #fcfcfc; padding: 2rem; }
.auth-card { width: 100%; max-width: 720px; background: #fcfcfc; border: 1.5px solid rgba(23, 24, 30, 0.08); border-radius: 16px; padding: 2rem; text-align: center; }
.title { font-size: 2rem; font-weight: 800; color: #17181e; }
.subtitle { color: #6b6b6b; margin: 0.5rem 0 1.5rem; }
.options { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 1rem; }
.option { display: flex; gap: 1rem; text-decoration: none; padding: 1rem; border: 1.5px solid rgba(23,24,30,0.08); border-radius: 12px; color: #17181e; background: #fff; transition: .2s; }
.option:hover { transform: translateY(-2px); border-color: rgba(23,24,30,0.2); }
.icon { font-size: 1.8rem; width: 48px; height: 48px; display: grid; place-items: center; background: #17181e; color: #fcfcfc; border-radius: 10px; }
.content h3 { margin: 0; font-size: 1.1rem; font-weight: 700; }
.content p { margin: 0.25rem 0 0; color: #6b6b6b; font-size: 0.9rem; }
.secondary-link { display: inline-block; margin-top: 1rem; color: #17181e; text-decoration: none; font-weight: 600; }
.secondary-link:hover { text-decoration: underline; }
</style>


