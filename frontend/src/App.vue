<template>
  <RouteProgress />
  <AppNavbar />
  <AppBreadcrumbs />
  <main>
    <transition name="fade" mode="out-in">
      <keep-alive include="showcase,professor-dashboard,aluno-dashboard">
        <router-view />
      </keep-alive>
    </transition>
  </main>
  <AppFooter />
  
</template>

<script setup lang="ts">
import AppNavbar from '@/shared/AppNavbar.vue'
import AppFooter from '@/shared/AppFooter.vue'
import AppBreadcrumbs from '@/shared/AppBreadcrumbs.vue'
import RouteProgress from '@/shared/RouteProgress.vue'
</script>

<style>
main { min-height: calc(100vh - 160px) }
.fade-enter-active, .fade-leave-active { transition: opacity .25s ease }
.fade-enter-from, .fade-leave-to { opacity: 0 }
</style>
