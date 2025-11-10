<template>
  <nav class="breadcrumbs" aria-label="Breadcrumb" v-if="items.length > 1">
    <ol>
      <li v-for="(it, i) in items" :key="i">
        <router-link v-if="i < items.length - 1" :to="it.to">{{ it.label }}</router-link>
        <span v-else aria-current="page">{{ it.label }}</span>
      </li>
    </ol>
  </nav>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const items = computed(() => {
  const list = route.matched.map(m => ({
    label: (m.meta?.title as string) || (m.name as string) || 'Início',
    to: { path: m.path || '/' }
  }))
  if (!list.length) return [{ label: 'Início', to: { path: '/' } }]
  return list
})
</script>

<style scoped>
.breadcrumbs { max-width: 1200px; margin: .75rem auto 0; padding: 0 1rem }
ol { display: flex; flex-wrap: wrap; gap: .5rem; list-style: none; color: #6b7280; font-size: .85rem }
li { display: inline-flex; gap: .5rem; align-items: center }
li+li:before { content: '›'; color: #9ca3af }
a { text-decoration: none; color: #6b7280 }
a:hover { color: #111827 }
span[aria-current="page"] { color: #111827; font-weight: 600 }
</style>


