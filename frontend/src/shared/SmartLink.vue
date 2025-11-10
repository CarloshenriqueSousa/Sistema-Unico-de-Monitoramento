<template>
  <router-link v-bind="$attrs" :to="to" @mouseenter="prefetch" @focus="prefetch">
    <slot />
  </router-link>
</template>

<script setup lang="ts">
import { defineProps } from 'vue'
import router from '@/router'
import type { RouteLocationRaw } from 'vue-router'

const props = defineProps<{ to: RouteLocationRaw }>()

const prefetch = () => {
  const r = router.resolve(props.to)
  const comp = r.matched[0]?.components?.default
  if (typeof comp === 'function') comp()
}
</script>

<style scoped>
/* herda estilos do router-link */
</style>


