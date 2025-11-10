<template>
  <header class="app-nav" :class="{ scrolled }">
    <nav class="container">
      <router-link class="brand" :to="{ name: 'showcase' }" aria-label="Ir para página inicial">
        <span class="logo">S.U.M</span>
        <span class="tag">Gestão Escolar</span>
      </router-link>

      <button class="hamburger" @click="menuOpen = !menuOpen" aria-label="Abrir menu" aria-expanded="menuOpen">
        <span></span><span></span><span></span>
      </button>

      <ul class="links" :class="{ open: menuOpen }">
        <li><router-link :to="{ name: 'showcase', hash: '#features' }">Funcionalidades</router-link></li>
        <li><router-link :to="{ name: 'showcase', hash: '#demos' }">Demonstrações</router-link></li>
        <li><router-link :to="{ name: 'showcase', hash: '#profiles' }">Perfis</router-link></li>
        <li><router-link class="cta" :to="{ name: 'entrar' }">Acessar</router-link></li>
      </ul>
    </nav>
  </header>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'

const menuOpen = ref(false)
const scrolled = ref(false)
const onScroll = () => { scrolled.value = window.scrollY > 12 }

onMounted(() => window.addEventListener('scroll', onScroll))
onUnmounted(() => window.removeEventListener('scroll', onScroll))
</script>

<style scoped>
.app-nav { position: sticky; top: 0; z-index: 1000; background: rgba(252,252,252,.7); backdrop-filter: blur(12px); border-bottom: 1px solid transparent; transition: all .2s ease; }
.app-nav.scrolled { background: rgba(252,252,252,.9); border-bottom-color: rgba(23,24,28,.08) }
.container { max-width: 1200px; margin: 0 auto; padding: .75rem 1rem; display: flex; align-items: center; justify-content: space-between }
.brand { display: inline-flex; gap: .5rem; align-items: center; text-decoration: none }
.logo { font-weight: 800; color: #17181c }
.tag { font-size: .75rem; color: #6b7280; background: rgba(23,24,28,.06); padding: .2rem .6rem; border-radius: .5rem }
.links { display: flex; gap: 1rem; align-items: center; list-style: none }
.links a { text-decoration: none; color: #6b7280; font-weight: 600 }
.links a:hover { color: #17181c }
.links .cta { background: #17181c; color: #fcfcfc; padding: .5rem .9rem; border-radius: .6rem }
.hamburger { display: none; background: none; border: 0; padding: .5rem; cursor: pointer }
.hamburger span { display: block; width: 22px; height: 2px; background: #17181c; margin: 4px 0 }
@media (max-width: 768px) {
  .hamburger { display: block }
  .links { position: absolute; top: 56px; right: 8px; flex-direction: column; background: #fff; border: 1px solid rgba(23,24,28,.08); border-radius: .75rem; padding: .5rem; display: none }
  .links.open { display: flex }
}
</style>


