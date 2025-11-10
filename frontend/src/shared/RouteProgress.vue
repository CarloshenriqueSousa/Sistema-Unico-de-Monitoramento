<template>
  <div class="route-progress" :style="{ transform: `scaleX(${progress})` }" role="status" aria-label="Carregando"></div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import router from '@/router'

const progress = ref(0)
let timer: number | null = null

const start = () => {
  progress.value = 0.08
  if (timer) window.clearInterval(timer)
  timer = window.setInterval(() => {
    // aproxima a barra do fim sem completá-la até o afterEach
    progress.value = Math.min(0.95, progress.value + (0.06 * (1 - progress.value)))
  }, 200)
}

const done = () => {
  if (timer) window.clearInterval(timer)
  progress.value = 1
  window.setTimeout(() => { progress.value = 0 }, 250)
  timer = null
}

onMounted(() => {
  router.beforeEach((to, from, next) => { start(); next() })
  router.afterEach(() => { done() })
})

onUnmounted(() => { if (timer) window.clearInterval(timer) })
</script>

<style scoped>
.route-progress { position: fixed; top: 0; left: 0; height: 3px; width: 100%; background: linear-gradient(90deg, #3b82f6, #10b981); transform-origin: left center; z-index: 1100; transition: transform .2s ease }
</style>


